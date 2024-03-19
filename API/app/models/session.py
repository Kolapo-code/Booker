from app.models import Base
from app.models.base_model import BaseModel
from app.utils.countries import ALL_COUNTRIES
from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from uuid import uuid4
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta

class Session(BaseModel, Base):
    __tablename__ = 'sessions'
    expiry_time = Column(Integer, nullable=False)
    regular_user_id = Column(String(60) , ForeignKey('regular_users.id'), nullable=True)
    premium_user_id = Column(String(60) , ForeignKey('premium_users.id'), nullable=True)

    def check_expiry(self):
        time_change = timedelta(seconds=self.expiry_time)
        new_time = self.created_at + time_change
        if new_time <= datetime.now():
            return False
        return True
