from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, DATETIME


class BaseModel:
    """The BaseModel class."""

    id = Column(String(60), primary_key=True)
    created_at = Column(DATETIME, default=datetime.now)
    updated_at = Column(DATETIME, default=datetime.now)

    def __init__(self, **kwargs) -> None:
        """A method that initializes the attributes."""
        if kwargs:
            for key, val in kwargs.items():
                if key not in ["id", "created_at", "updated_at"]:
                    setattr(self, key, val)
        self.id = str(uuid4())

    def save(self):
        """A method that saves an instance."""
        from app import storage

        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def update(self, **data):
        """A method that updates an instance."""
        for key, val in data.items():
            if key not in ["created_at", "updated_at", "id"]:
                setattr(self, key, val)

    def to_dict(self):
        """A method that sets up a dictionary."""
        new_dict = dict(
            filter(lambda x: not x[0].startswith("_"), self.__dict__.items())
        )
        return new_dict
