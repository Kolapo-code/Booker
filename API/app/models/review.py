from app.models import Base
from app.models.base_model import BaseModel
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DATETIME, Integer, Boolean, Enum, ForeignKey


class Review(BaseModel, Base):
    """The Review model"""

    __tablename__ = "reviews"
    title = Column(String(60))
    content = Column(String(1500))
    reviewer_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    workspace_id = Column(String(60), ForeignKey("workspaces.id"), nullable=False)
