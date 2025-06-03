from typing import Optional

from pydantic import BaseModel, EmailStr, constr


class RegisterUserSpec(BaseModel):
    username: constr(min_length=3, max_length=30)
    email: EmailStr
    password: constr(min_length=6)


class LoginSpec(BaseModel):
    email: EmailStr
    password: str


class UpdateUserSpec(BaseModel):
    username: Optional[constr(min_length=3, max_length=30)] = None
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=6)] = None
