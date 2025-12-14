from datetime import datetime
from typing import Literal, Optional

from .base import BaseEntity


class Document_knowladge(BaseEntity):
    agent_id: Optional[int] = None
    title: str
    description: str
    file_path: str
    file_format: Literal["text", "json", "markdown"]
    file_size: int
    status: Literal["uploaded", "processed", "failed"] = "processed"
    updated_at: datetime
