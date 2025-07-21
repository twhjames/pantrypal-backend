from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, constr

from src.core.account.specs import LoginSpec, RegisterUserSpec, UpdateUserSpec


class RegisterUserIn(BaseModel):
    username: constr(min_length=3, max_length=30)
    email: EmailStr
    password: constr(min_length=6)

    def to_spec(self) -> RegisterUserSpec:
        return RegisterUserSpec(
            username=self.username,
            email=self.email,
            password=self.password,
        )


class LoginUserIn(BaseModel):
    email: EmailStr
    password: str

    def to_spec(self) -> LoginSpec:
        return LoginSpec(email=self.email, password=self.password)


class UpdateUserIn(BaseModel):
    username: Optional[constr(min_length=3, max_length=30)] = None
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=6)] = None

    def to_spec(self) -> UpdateUserSpec:
        return UpdateUserSpec(
            username=self.username, email=self.email, password=self.password
        )


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    is_admin: bool


class AuthTokenOut(BaseModel):
    user_id: int
    token: str
    token_type: str = "Bearer"
    expires_at: datetime
