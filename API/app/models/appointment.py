from app.models import Base
from datetime import datetime
from app.models.base_model import BaseModel
from sqlalchemy import Column, String, DATETIME, Integer, Boolean, Enum, ForeignKey


class Appointment(BaseModel, Base):
    """The Appointement model"""

    __tablename__ = "appointments"
    date = Column(DATETIME, default=datetime.now)
    range = Column(Integer)
    status = Column(Enum("Pending", "Verified", "Canceled"), default="Pending")
    attended = Column(Boolean, default=False)
    verify = Column(Boolean, default=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    workspace_id = Column(String(60), ForeignKey("workspaces.id"), nullable=False)
