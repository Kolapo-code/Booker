from app.models import Base
from datetime import datetime
from app.models.user import BaseModel
from app.utils.countries import ALL_COUNTRIES
from sqlalchemy import Column, String, Date, Boolean, Enum, ForeignKey


class PremiumAccount(BaseModel, Base):
    """The PremiumAccount model."""

    __tablename__ = "premium_account"
    field = Column(String(100), nullable=False)
    location = Column(String(100), nullable=True)
    biography = Column(String(300), nullable=False)
    subscription_start_date = Column(Date, default=datetime.now)
    subscription_end_date = Column(Date)
    subscription_plan = Column(Enum("Montly", "Yearly"))
    subscription_status = Column(
        Enum("Pending", "Active", "Suspended", default="Pending"),
        nullable=False,
    )
    auto_renewal = Column(Boolean, default=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
