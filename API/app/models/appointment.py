from app.models.base_model import BaseModel
from sqlalchemy import Column, String, Date, Integer, Boolean, Enum, ForeignKey


class Appointment(BaseModel):
    """The Appointement model"""

    date = Column(Date)
    range = Column(Integer)
    status = Column(Enum('Pending', 'Verified', 'Blocked'))
    attended = Column(Boolean)
    verify = Column(Boolean)
    user_id = Column(String(60), ForeignKey('regular_users.id'), nullable=False)
