from datetime import datetime

from pydantic import BaseModel


class BaseEntity(BaseModel):
    id: int
    created_at: datetime
