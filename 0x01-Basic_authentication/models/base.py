#!/usr/bin/env python3
"""Base module
"""
from datetime import datetime
from typing import TypeVar, List, Iterable, Optional, Dict, Any
from os import path
import json
import uuid

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATA: Dict[str, Dict[str, 'Base']] = {}

BaseType = TypeVar('BaseType', bound='Base')


class Base:
    """Base class"""

    def __init__(self, *args: List[Any], **kwargs: Dict[str, Any]):
        """Initialize a Base instance"""
        s_class = self.__class__.__name__
        if DATA.get(s_class) is None:
            DATA[s_class] = {}

        self.id: str = kwargs.get('id', str(uuid.uuid4()))
        self.created_at: datetime = datetime.strptime(kwargs.get('created_at'), TIMESTAMP_FORMAT) if kwargs.get('created_at') else datetime.utcnow()
        self.updated_at: datetime = datetime.strptime(kwargs.get('updated_at'), TIMESTAMP_FORMAT) if kwargs.get('updated_at') else datetime.utcnow()

    def __eq__(self, other: BaseType) -> bool:
        """Check equality between two Base instances"""
        if not isinstance(other, Base):
            return False
        return self.id == other.id

    def to_json(self, for_serialization: bool = False) -> Dict[str, Any]:
        """Convert the object to a JSON dictionary"""
        result: Dict[str, Any] = {}
        for key, value in self.__dict__.items():
            if not for_serialization and key.startswith('_'):
                continue
            result[key] = value.strftime(TIMESTAMP_FORMAT) if isinstance(value, datetime) else value
        return result

    @classmethod
    def load_from_file(cls):
        """Load all objects from file"""
        s_class = cls.__name__
        file_path = f".db_{s_class}.json"
        DATA[s_class] = {}
        if not path.exists(file_path):
            return

        with open(file_path, 'r') as f:
            try:
                objs_json = json.load(f)
                for obj_id, obj_json in objs_json.items():
                    DATA[s_class][obj_id] = cls(**obj_json)
            except json.JSONDecodeError:
                pass

    @classmethod
    def save_to_file(cls):
        """Save all objects to file"""
        s_class = cls.__name__
        file_path = f".db_{s_class}.json"
        objs_json = {obj_id: obj.to_json(True) for obj_id, obj in DATA[s_class].items()}

        with open(file_path, 'w') as f:
            json.dump(objs_json, f)

    def save(self):
        """Save current object"""
        s_class = self.__class__.__name__
        self.updated_at = datetime.utcnow()
        DATA[s_class][self.id] = self
        self.__class__.save_to_file()

    def remove(self):
        """Remove object"""
        s_class = self.__class__.__name__
        if self.id in DATA[s_class]:
            del DATA[s_class][self.id]
            self.__class__.save_to_file()

    @classmethod
    def count(cls) -> int:
        """Count all objects"""
        s_class = cls.__name__
        return len(DATA[s_class])

    @classmethod
    def all(cls) -> Iterable[BaseType]:
        """Return all objects"""
        return cls.search()

    @classmethod
    def get(cls, id: str) -> Optional[BaseType]:
        """Return one object by ID"""
        s_class = cls.__name__
        return DATA[s_class].get(id)

    @classmethod
    def search(cls, attributes: Dict[str, Any] = {}) -> List[BaseType]:
        """Search all objects with matching attributes"""
        s_class = cls.__name__

        def _search(obj: BaseType) -> bool:
            return all(getattr(obj, k) == v for k, v in attributes.items())

        return list(filter(_search, DATA[s_class].values()))
