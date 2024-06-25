"""
Abstract base class for all models
"""

from datetime import datetime
from typing import Any, Optional
import uuid
from abc import abstractmethod
from src import db

class Base(db.Model):
    __abstract__ = True  # This prevents SQLAlchemy from creating a table for this class

    id = db.Column(db.String(36), primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    def __init__(
        self,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        **kwargs,
    ) -> None:
        """
        Base class constructor
        If kwargs are provided, set them as attributes
        """
        super().__init__(**kwargs)

        if kwargs:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    continue
                setattr(self, key, value)

        self.id = str(id or uuid.uuid4())
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    @classmethod
    def get(cls, id) -> "Any | None":
        """
        This is a common method to get a specific object
        of a class by its id

        If a class needs a different implementation,
        it should override this method
        """
        return cls.query.get(id)

    @classmethod
    def get_all(cls) -> list["Any"]:
        """
        This is a common method to get all objects of a class

        If a class needs a different implementation,
        it should override this method
        """
        return cls.query.all()

    @classmethod
    def delete(cls, id) -> bool:
        """
        This is a common method to delete a specific
        object of a class by its id

        If a class needs a different implementation,
        it should override this method
        """
        obj = cls.get(id)
        if not obj:
            return False
        db.session.delete(obj)
        db.session.commit()
        return True

    @abstractmethod
    def to_dict(self) -> dict:
        """Returns the dictionary representation of the object"""

    @staticmethod
    @abstractmethod
    def create(data: dict) -> Any:
        """Creates a new object of the class"""

    @staticmethod
    @abstractmethod
    def update(entity_id: str, data: dict) -> Any | None:
        """Updates an object of the class"""
