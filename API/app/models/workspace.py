from app.models import Base
from app.models.base_model import BaseModel
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DATETIME, Integer, Boolean, Enum, ForeignKey
from app.config import SCHEDULES


class Workspace(BaseModel, Base):
    """The Workspace model"""

    __tablename__ = "workspaces"
    title = Column(String(60), nullable=False)
    field = Column(String(60), nullable=False)
    description = Column(String(500), nullable=True)
    picture = Column(String(256), nullable=True)
    schedules = Column(String(256), default=SCHEDULES)
    location = Column(String(256), nullable=True)
    contact = Column(String(256), nullable=True)

    premium_account_id = Column(
        String(60), ForeignKey("premium_accounts.id"), nullable=False
    )
    reviews = relationship("Review", backref="workspace", cascade="all, delete-orphan")
    appointments = relationship(
        "Appointment", backref="workspace", cascade="all, delete-orphan"
    )
