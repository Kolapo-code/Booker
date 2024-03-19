from app.models import Base
from app.models.user import User
from app.utils.countries import ALL_COUNTRIES
from sqlalchemy import Column, String, Date, Boolean, Enum
from uuid import uuid4


class PremiumUser(User, Base):
    __tablename__ = "premium_users"
    birth_date = Column(Date, nullable=True)
    field = Column(String(100), nullable=False)
    location = Column(Enum(*ALL_COUNTRIES, name="countries"), nullable=True)
    biography = Column(String(300), nullable=False)
    subscription_start_date = Column(Date)
    subscription_end_date = Column(Date)
    subscription_plan = Column(String(300))
    subscription_status = Column(
        Enum("Pending", "Active", "Suspended", name="subscription_status"),
        nullable=False,
    )
    auto_renewal = Column(Boolean, default=False)
    ban = Column(Boolean, default=False)
