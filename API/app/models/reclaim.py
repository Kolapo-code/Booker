from app.models import Base
from app.utils.countries import ALL_COUNTRIES
from sqlalchemy import Column, String, DATETIME, Boolean, Enum, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel
from sqlalchemy import Column, String


class Reclaim(BaseModel, Base):
    """The Reclaim model"""

    __tablename__ = "reclaims"
    subject = Column(String(200), nullable=False)
    description = Column(String(2000), nullable=False)
    status = Column(Enum("Pending", "Resolved"), default="Pending")
    reclaimed_id = Column(String(60), nullable=False)
    reclaimer_id = Column(String(60), ForeignKey("users.id"), nullable=False)
