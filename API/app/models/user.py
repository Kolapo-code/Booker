from app.models import Base
from sqlalchemy import Column, String
from uuid import uuid4

class User(Base):
    """The User model"""
    __tablename__ = 'users'
    id = Column(String(60), primary_key=True)
    name = Column(String(60))
    age = Column(String(60), nullable=True)

    def __init__(self, **kwargs) -> None:
        if kwargs:
            for key, val in kwargs.items():
                setattr(self, key, val)
            self.id = str(uuid4())

    def to_dict(self):
        new_dict =  self.__dict__.copy()
        del new_dict["_sa_instance_state"]
        return new_dict
