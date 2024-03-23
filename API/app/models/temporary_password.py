from app.models import Base
from app.models.base_model import BaseModel
from app.utils.countries import ALL_COUNTRIES
from sqlalchemy import Column, String, Integer, ForeignKey, Enum
import base64
from datetime import datetime, timedelta
from app.utils.helper import hash_to_sha256


class TemporaryPassword(BaseModel, Base):
    """The TemporaryPassword model"""

    __tablename__ = "temporary_passwords"
    __password = Column(String(128))
    expiry_time = Column(Integer, default=600)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)

    def __init__(self, **kwargs) -> None:
        filtered = dict(filter(lambda x: x[0] != "password", kwargs.items()))
        super().__init__(**filtered)
        self.password = kwargs["password"]

    def check_expiry(self):
        time_change = timedelta(seconds=self.expiry_time)
        new_time = self.created_at + time_change
        if new_time <= datetime.now():
            return False
        return True

    @property
    def password(self):
        if self.check_expiry():
            return self.__password
        return None

    @password.setter
    def password(self, value):
        if value is None or type(value) is not bytes:
            return "Unable to set password"
        decoded_password = base64.b64decode(value)
        passw = hash_to_sha256(decoded_password.decode("utf-8"))
        self.__password = passw
