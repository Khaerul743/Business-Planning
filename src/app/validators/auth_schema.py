from pydantic import BaseModel, EmailStr


class AuthBase(BaseModel):
    email: EmailStr


class RegisterIn(AuthBase):
    name: str
    password: str


class RegisterOut(AuthBase):
    name: str
