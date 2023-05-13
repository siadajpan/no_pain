from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class ShowUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str

    class Config:
        orm_mode = True
