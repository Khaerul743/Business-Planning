from typing import Optional

from pydantic import BaseModel


class AddBusinessIn(BaseModel):
    name: str
    owner_name: Optional[str] = None
    phone_number: str
    description: str
    address: str


class BusinessUpdateIn(BaseModel):
    name: Optional[str] = None
    owner_name: Optional[str] = None
    phone_number: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
