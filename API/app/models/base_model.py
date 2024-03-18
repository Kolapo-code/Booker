from sqlalchemy import Column, String, DATETIME
from datetime import datetime
from uuid import uuid4


class BaseModel:
    id = Column(String(60), primary_key=True)
    created_at = Column(DATETIME, default=datetime.now)
    updated_at = Column(DATETIME, default=datetime.now)

    def __init__(self, **kwargs) -> None:
        if kwargs:
            for key, val in kwargs.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(self, key, val)
            self.id = str(uuid4())

    def save(self):
        from app import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def update(self, **data):
        for key, val in data.items():
            if key not in ['created_at', 'updated_at', 'id']:
                setattr(self, key, val)

    def to_dict(self):
        new_dict =  self.__dict__.copy()
        del new_dict["_sa_instance_state"]
        return new_dict
