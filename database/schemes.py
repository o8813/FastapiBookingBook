from pydantic import BaseModel, Field, model_validator
from enum import Enum
from datetime import date, datetime

class StatusChoices(str, Enum):
    pending = 'pending'
    confirmed = 'confirmed'
    canceled = 'canceled'

class BookingCreateScheme(BaseModel):
    hotel_id: int = Field(gt=0)
    room_id: int = Field(gt=0)
    checkin: date | datetime
    checkout: date | datetime

    @model_validator(mode='after')
    def validate_dates(self):
        if self.checkin >= self.checkout:
            raise ValueError('Check in date should not be ascending than checkout date!')

        if self.checkin < date.today():
            raise ValueError('You should not book from late date')

        return self

class BookingUpdateScheme(BaseModel):
    checkin: date | datetime | None
    checkout: date | datetime | None

class BookingResponseScheme(BaseModel):
    id: str
    user_id: int

    hotel_id: int
    hotel_name: str
    room_id: int
    room_number: int
    room_price: float
    checkin: date | datetime
    checkout: date | datetime

    total_price: float
    status: StatusChoices = Field(default=StatusChoices.pending)
    created_date: datetime
    updated_date: datetime