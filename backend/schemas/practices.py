from typing import Optional

from pydantic import BaseModel


class PracticeCreate(BaseModel):
    name: str
    street: str
    street_number: str
    apartment_number: Optional[str]


class PracticeShow(BaseModel):
    name: str
    street: str
    street_number: str
    apartment_number: Optional[str]

    class Config:
        orm_mode = True
