from app.models import Base
from app.models.base_model import BaseModel
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DATETIME, Integer, Boolean, Enum, ForeignKey


class Reclaim(BaseModel, Base):
    """The Reclaim model"""

    __tablename__ = "Reclaims"
    subject = Column(String(200))
    content = Column(String(2500))
    reclaimer_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    reclaimed_id = Column(String(60), ForeignKey("users.id"), nullable=False)
