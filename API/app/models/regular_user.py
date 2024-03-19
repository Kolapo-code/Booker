from app.models import Base
from app.models.user import User
from app.utils.countries import ALL_COUNTRIES
from sqlalchemy import Column, String, Date, Boolean, Enum
from uuid import uuid4

class RegularUser(User, Base):
    __tablename__ = 'regular_users'
    birth_date = Column(Date, nullable=False)
    location = Column(Enum(*ALL_COUNTRIES), nullable=True)
    # account_status = Column(String(100)) WHY DID WE ADD THIS!!!!
    ban = Column(Boolean, default=False)
