from app.models import Base
from app.models.base_model import BaseModel
from sqlalchemy import Column, String
from uuid import uuid4

class User(BaseModel, Base):
    """The User model"""
    __tablename__ = 'users'
    name = Column(String(60))
    age = Column(String(60), nullable=True)
