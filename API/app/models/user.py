from app.models import Base
from app.utils.countries import ALL_COUNTRIES
from sqlalchemy import Column, String, Date, Boolean, Enum
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel
from sqlalchemy import Column, String
from app.utils.helper import hash_to_sha256
import base64


class User(BaseModel, Base):
    """The User model"""

    __tablename__ = "users"
    first_name = Column(String(60))
    last_name = Column(String(60))
    email = Column(String(128))
    __password = Column(String(128))
    picture = Column(String(256), nullable=True)
    birth_date = Column(Date, nullable=False)
    location = Column(Enum(*ALL_COUNTRIES), nullable=True)
    ban = Column(Boolean, default=False)
    token = Column(String(60), nullable=True)
    valid = Column(Boolean, default=False)
    admin_account = relationship(
        "AdminAccount", backref="user", cascade="all, delete-orphan"
    )
    premium_account = relationship(
        "PremiumAccount", backref="user", cascade="all, delete-orphan"
    )
    sessions = relationship("Session", backref="user", cascade="all, delete-orphan")
    appointment = relationship("Appointment", backref="user", cascade="all, delete-orphan")

    def __init__(self, **kwargs) -> None:
        """A method that intializes attributes."""
        filtered = dict(filter(lambda x: x[0] != "password", kwargs.items()))
        super().__init__(**filtered)
        self.password = kwargs["password"]

    @property
    def password(self):
        """A method that gets the password."""
        return "You can not get the password it is indeed private"

    @password.setter
    def password(self, value):
        """A method that sets the password."""
        if value is None or type(value) is not bytes:
            return "Unable to set password"
        decoded_password = base64.b64decode(value)
        passw = hash_to_sha256(decoded_password.decode("utf-8"))
        self.__password = passw

    def check_password(self, password):
        """A method responsible for validating the password, by hashing
        the given password and comparing it to the saved password in db."""
        if password is None:
            return False
        if type(password) is not bytes:
            return False
        decoded_password = base64.b64decode(password)
        hashed_password = hash_to_sha256(decoded_password.decode("utf-8"))
        return True if self.__password == hashed_password else False
