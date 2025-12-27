# src/infra/context/request_context.py
from contextvars import ContextVar
from typing import Optional

current_user_id: ContextVar[Optional[int]] = ContextVar("current_user_id", default=None)
current_user_email: ContextVar[Optional[str]] = ContextVar(
    "current_user_email", default=None
)
current_user_role: ContextVar[Optional[str]] = ContextVar(
    "current_user_role", default=None
)
