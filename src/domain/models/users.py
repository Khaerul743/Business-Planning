from typing import Literal, Optional

from .base import BaseEntity


class User(BaseEntity):
    avatar: Optional[str] = None
    name: str
    email: str
    password: str
    status: Literal["active", "inactive"] = "active"
