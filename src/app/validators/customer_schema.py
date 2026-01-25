from pydantic import BaseModel


class InsertNewCustomer(BaseModel):
    wa_id: str
    name: str
    phone_number: str
    enable_ai: bool = True
