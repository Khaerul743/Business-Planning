from typing import Literal, Optional

from pydantic import BaseModel


class AddBusinessKnowladgeIn(BaseModel):
    category: str
    category_description: str
    content: str


class UpdateBusinessKnowladgeIn(BaseModel):
    category: Optional[str] = None
    category_description: Optional[str] = None
    content: Optional[str] = None
