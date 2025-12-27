from typing import Literal

from pydantic import BaseModel, EmailStr


class AuthBase(BaseModel):
    email: EmailStr


class RegisterIn(AuthBase):
    name: str
    password: str


class RegisterOut(AuthBase):
    name: str


class LoginIn(AuthBase):
    password: str


class LoginOut(AuthBase):
    name: str
    role: Literal["admin", "user"] = "user"
