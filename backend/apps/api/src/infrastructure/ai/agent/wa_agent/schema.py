from pydantic import BaseModel


class BusinessDetailInformation(BaseModel):
    business_name: str
    business_desc: str
    business_location: str


class BusinessKnowladgeContent(BaseModel):
    category_description: str
    content: str


class DocumentRagDetail(BaseModel):
    title: str
    description: str
