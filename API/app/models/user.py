from app.models import Base
from app.models.base_model import BaseModel
from sqlalchemy import Column, String
from uuid import uuid4

class User(BaseModel, Base):
    """The User model"""
    __tablename__ = 'users'
    first_name = Column(String(60))
    last_name = Column(String(60))
    email = Column(String(128))
    password = Column(String(128))
    picture = Column(String(256), nullable=True)
