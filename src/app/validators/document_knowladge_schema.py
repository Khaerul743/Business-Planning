from typing import Literal

from pydantic import BaseModel


class AddDocumentKnowladge(BaseModel):
    title: str
    description: str
    file_path: str
    file_format: str
    file_size: int
    status: Literal["processed", "uploaded", "failed"] = "processed"
