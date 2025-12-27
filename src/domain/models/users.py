from typing import Literal, Optional

from .base import BaseEntity


class User(BaseEntity):
    avatar: Optional[str] = None
    name: str
    email: str
    role: Literal["admin", "user"] = "user"
    status: Literal["active", "inactive"] = "active"
