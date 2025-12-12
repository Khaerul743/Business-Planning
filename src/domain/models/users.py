from typing import Literal, Optional

from .base import BaseModelSchema


class User(BaseModelSchema):
    avatar: Optional[str] = None
    name: str
    email: str
    password: str
    status: Literal["active", "inactive"] = "active"
