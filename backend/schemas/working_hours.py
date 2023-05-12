from datetime import datetime

from pydantic import BaseModel, validator

from schemas.types import DayOfWeek


class WorkingHoursCreate(BaseModel):
    user_id: int
    practice_id: int
    day_of_week: str
    start_time: str
    end_time: str

    @validator("day_of_week")
    def ensure_correct_day(cls, value):
        if value not in (day for (i, day) in DayOfWeek):
            raise ValueError("Wrong day of week")
        return value

    @validator("start_time", "end_time")
    def ensure_correct_time(cls, value):
        try:
            datetime.strptime(value, "%H:%M")
        except ValueError as e:
            raise ValueError("Wrong time format")
        return value

    # TODO Add validator checking if end time > start time

class WorkingHoursShow(BaseModel):
    day_of_week: str
    start_time: str
    end_time: str

    class Config:
        orm_mode = True
