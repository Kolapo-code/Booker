from app.models import Base
from app.models.user import BaseModel
from app.utils.countries import ALL_COUNTRIES
from sqlalchemy import Column, String, Date, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4


class PremiumAccount(BaseModel, Base):
    """The PremiumAccount model."""

    __tablename__ = "premium_account"
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    field = Column(String(100), nullable=False)  # General field of activity.
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
