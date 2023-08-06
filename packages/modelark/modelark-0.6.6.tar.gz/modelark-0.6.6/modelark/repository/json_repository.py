import os
import time
import json
import fcntl
from uuid import uuid4
from pathlib import Path
from collections import defaultdict
from contextlib import contextmanager
from typing import Dict, List, Tuple, Any, Callable, Generic, Union, cast
from ..common import (
    T, R, L, Locator, DefaultLocator, Editor, DefaultEditor)
from ..filterer import Filterer, FunctionParser, Domain
from .repository import Repository


class JsonRepository(Repository, Generic[T]):
    def __init__(self,
                 data_path: str,
                 collection: str,
                 constructor: Callable[..., T],
                 filterer: Filterer = None,
                 locator: Locator = None,
                 editor: Editor = None) -> None:
        self.data_path = data_path
        self.collection = collection
        self.constructor: Callable[..., T] = constructor
        self.filterer = filterer or FunctionParser()
        self.locator = locator or DefaultLocator()
        self.editor = editor or DefaultEditor()

    async def setup(self) -> None:
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with locked_open(str(self.file_path), 'w') as f:
                f.write("{}")

    async def add(self, item: Union[T, List[T]]) -> List[T]:
        await self.setup()

        items = item if isinstance(item, list) else [item]

        data: Dict[str, Any] = defaultdict(lambda: {})
        with locked_open(str(self.file_path), 'r+') as f:
            data.update(json.loads(f.read()))

            for item in items:
                item.updated_at = int(time.time())
                item.updated_by = self.editor.reference
                item.created_at = item.created_at or item.updated_at
                item.created_by = item.created_by or item.updated_by

                data[self.collection][item.id] = vars(item)

            f.seek(f.truncate(0))
            f.write(json.dumps(data, indent=2))

        return items

    async def remove(self, item: Union[T, List[T]]) -> bool:
        if not self.file_path.exists():
            return False

        items = item if isinstance(item, list) else [item]

        with locked_open(str(self.file_path), 'r+') as f:
            data = json.loads(f.read())

            deleted = False
            for item in items:
                deleted_item = data[self.collection].pop(item.id, None)
                deleted = bool(deleted_item) or deleted

            f.seek(f.truncate(0))
            f.write(json.dumps(data, indent=2))

        return deleted

    async def count(self, domain: Domain = None) -> int:
        if not self.file_path.exists():
            return 0

        with locked_open(str(self.file_path), 'r') as f:
            data = json.loads(f.read())

            count = 0
            domain = domain or []
            filter_function = self.filterer.parse(domain)
            for item_dict in list(data[self.collection].values()):
                item = self.constructor(**item_dict)
                if filter_function(item):
                    count += 1

            return count

    async def search(self, domain: Domain,
                     limit: int = None, offset: int = None,
                     order: str = None) -> List[T]:
        items: List[T] = []
        if not self.file_path.exists():
            return items

        with locked_open(str(self.file_path), 'r') as f:
            data = json.loads(f.read())
            items_dict = data.get(self.collection, {})

            filter_function = self.filterer.parse(domain)
            for item_dict in items_dict.values():
                item = self.constructor(**item_dict)

                if filter_function(item):
                    items.append(item)

            if offset is not None:
                items = items[offset:]
            if limit is not None:
                items = items[:limit]
            if not order:
                return items

            fields = order.lower().split(',')
            for field in reversed(fields):
                key, *direction = field.split()
                items = cast(List[T], sorted(
                    items, key=lambda item: getattr(item, key),
                    reverse=('desc' in direction)))

            return items

    @property
    def file_path(self) -> Path:
        return (Path(self.data_path) / self.locator.zone /
                self.locator.location / f"{self.collection}.json")


@contextmanager
def locked_open(filename, mode='r'):
    with open(filename, mode) as file:
        fcntl.flock(file, fcntl.LOCK_EX)
        yield file
        fcntl.flock(file, fcntl.LOCK_UN)
