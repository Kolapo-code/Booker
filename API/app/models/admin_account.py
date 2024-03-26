from app.models import Base
from app.models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey


class AdminAccount(BaseModel, Base):
    """The AdminAccount model."""

    __tablename__ = "admin_account"
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
