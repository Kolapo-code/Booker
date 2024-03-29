from app.utils.schedules import SCHEDULES
from app.models import Base
from app.models.base_model import BaseModel
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DATETIME, Integer, Boolean, Enum, ForeignKey
import json


class Workspace(BaseModel, Base):
    """The Workspace model"""

    __tablename__ = "workspaces"
    title = Column(String(60), nullable=False)
    field = Column(String(60), nullable=False)
    description = Column(String(500), nullable=True)
    picture = Column(String(256), nullable=True)
    schedules = Column(String(2000), default=SCHEDULES)
    location = Column(String(256), nullable=True)
    contact = Column(String(256), nullable=True)
    appointment_per_hour = Column(Integer, default=1)

    premium_account_id = Column(
        String(60), ForeignKey("premium_accounts.id"), nullable=False
    )
    reviews = relationship("Review", backref="workspace", cascade="all, delete-orphan")
    appointments = relationship(
        "Appointment", backref="workspace", cascade="all, delete-orphan"
    )

    def busy_hours(self):
        frequency_hours = {}
        busy_list = list(filter(lambda x:  isinstance(x, str), list(
            map(
                lambda x: str(x.date)[:-6] if ( str(x.date)[:-6] not in frequency_hours and\
                    frequency_hours.update({str(x.date)[:-6]: 0})) or\
                    frequency_hours[str(x.date)[:-6]] == self.appointment_per_hour - 1 else\
                        frequency_hours.update({str(x.date)[:-6]: frequency_hours[str(x.date)[:-6]] + 1}),
                        self.appointments
            )
        )))
        return busy_list

    def available_date(self, date):
        schedules = json.loads(self.schedules)
        if "days" in schedules:
            schedules = schedules["days"]
        day = date.strftime("%A").lower()
        hour = date.strftime("%H:%M")
        if day not in schedules or schedules[day] == {}:
            return False
        hour = datetime.strptime(hour, "%H:%M")
        try:
            start = datetime.strptime(schedules[day]["from"], "%H:%M")
            end = datetime.strptime(schedules[day]["to"], "%H:%M")
            if 'break' in schedules[day] and schedules[day]['break']:
                break_start = datetime.strptime(schedules[day]['break']["from"], "%H:%M")
                break_end = datetime.strptime(schedules[day]['break']["to"], "%H:%M")
                if start <= hour <= break_start or break_end <= hour <= end:
                    return True
            else:
                if start <= hour <= end:
                    return True
        except Exception:
            return False
        return False
