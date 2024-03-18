from app.models import Base
from app.models.user import User
from sqlalchemy import Column, String
from uuid import uuid4

class PremiumUser(User, Base):
    __tablename__ = 'premium_users'
