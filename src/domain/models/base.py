from datetime import datetime

from pydantic import BaseModel


class BaseModelSchema(BaseModel):
    id: int
    created_at: datetime
