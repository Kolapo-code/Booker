from app.models import Base
from app.models.user import User
from app.models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey

class AdminAccount(BaseModel, Base):
    """The AdminUser model"""

    __tablename__ = "admin_account"
    user_id = Column(String(60), ForeignKey('regular_users.id'), nullable=False)


    # def list_appointments():
    #     """A method that lists all the appointments that exist."""
    #     appointments = storage.get(cls='Appointment')
    #     return appointments
