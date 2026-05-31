from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from .base import BaseEntity


class DocumentKnowladge(BaseEntity):
    agent_id: Optional[UUID] = None
    title: str
    description: str
    file_path: str
    file_format: Literal["pdf", "docs", "txt"]
    file_size: int
    status: Literal["uploaded", "processed", "failed"] = "processed"
    updated_at: datetime
