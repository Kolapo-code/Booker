from app.models import Base
from app.models.base_model import BaseModel
from sqlalchemy import Column, String
from uuid import uuid4

class User(BaseModel):
    """The User model"""
    first_name = Column(String(60))
    last_name = Column(String(60))
    email = Column(String(128))
    __password = Column(String(128))
    picture = Column(String(256), nullable=True)

    def __init__(self, **kwargs) -> None:
        filtered = dict(filter(lambda x: x[0] != 'password', kwargs.items() ))
        super().__init__(**filtered)
        self.password = kwargs['password']

    @property
    def password(self):
        return 'You can not get the password it is indeed private'

    @password.setter
    def password(self, value):
        self.__password = value

    def check_password(self, given_password):
        """decrypting_hashing..."""
        return given_password == self.password
