from pydantic import BaseModel
from typing import Dict, Any


class BaseJob(BaseModel):
    queue_id: str
    type: str
    retry: int = 0
    max_retry: int = 3
    job_payload: Dict[str, Any]
