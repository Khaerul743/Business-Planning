from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class BaseEntity(BaseModel):
    id: UUID
    created_at: datetime
