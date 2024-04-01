from app.models import Base
from datetime import datetime
from app.models.user import BaseModel
from sqlalchemy import Column, String, Date, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship

class PremiumAccount(BaseModel, Base):
    """The PremiumAccount model."""

    __tablename__ = "premium_accounts"
    field = Column(String(100), nullable=False)
    biography = Column(String(300), nullable=False)
    subscription_start_date = Column(Date, default=datetime.now)
    subscription_end_date = Column(Date)
    subscription_plan = Column(Enum("Monthly", "Yearly"))
    subscription_status = Column(
        Enum("Pending", "Active", "Suspended", default="Pending"),
        nullable=False,
    )
    auto_renewal = Column(Boolean, default=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    workspaces = relationship('Workspace',
                           backref='premium_account',
                           cascade="all, delete-orphan")
    payments = relationship('Payment',
                           backref='premium_account',
                           cascade="all, delete-orphan")
