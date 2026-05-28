from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from .base import BaseEntity


class BusinessKnowladge(BaseEntity):
    business_id: Optional[UUID] = None
    category: str
    category_description: str
    content: str
    updated_at: datetime
