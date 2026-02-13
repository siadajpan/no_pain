from typing import List, Optional
from fastapi import Request
from no_pain.backend.core.config import settings
from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional


class UserCreate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    repeat_password: Optional[str] = None
    role: Optional[str] = "patient"
    street_address: Optional[str] = None
    city: Optional[str] = None
    postcode: Optional[str] = None
    practice_name: Optional[str] = None
    phone: Optional[str] = None

    @model_validator(mode='after')
    def validate_names_based_on_role(self):
        role = self.role
        if role == "practice":
            if not self.practice_name:
                raise ValueError("Practice Name is required")
            if not self.street_address:
                raise ValueError("Street Address is required")
            if not self.city:
                raise ValueError("City is required")
            if not self.postcode:
                raise ValueError("Postcode is required")
        else:
            # Patient or Doctor or default
            if not self.first_name:
                raise ValueError("First Name is required")
            if len(self.first_name) < 2:
                raise ValueError("First Name needs to be at least 2 characters")
            if not self.last_name:
                raise ValueError("Last Name is required")
            if len(self.last_name) < 2:
                raise ValueError("Last Name needs to be at least 2 characters")
        return self

    @field_validator("email")
    def is_email_valid(cls, email):
        if not email:
            raise ValueError("Email is required")
        if not EmailStr._validate(email):
            raise ValueError("Invalid email address")
        return email

    @field_validator("password")
    def is_password_valid(cls, password):
        if not password:
            raise ValueError("Password is required")
        if len(password) < settings.PASSWORD_LENGTH:
            raise ValueError(
                f"Password needs to be at least {settings.PASSWORD_LENGTH} characters"
            )
        return password

    @field_validator("repeat_password")
    def is_repeat_password_valid(cls, repeat_password, info):
        if not repeat_password:
            raise ValueError("Repeat password is required")
        if "password" in info.data and repeat_password != info.data["password"]:
            raise ValueError("Passwords don't match")
        return repeat_password


class UserShow(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True
