from typing import Literal
from dataclasses import dataclass

# Agent configuration


@dataclass
class AgentConfiguration:
    base_prompt: str
    tone: Literal["friendly", "formal", "casual", "profesional"]


@dataclass
class BusinessDetailInformation:
    business_name: str
    business_desc: str
    business_location: str


@dataclass
class BusinessKnowladgeContent:
    category_description: str
    content: str


@dataclass
class DocumentRagDetail:
    title: str
    description: str


@dataclass
class BusinessContext:
    business_detail_information: BusinessDetailInformation | None
    business_knowladge_content: dict[str, BusinessKnowladgeContent] | None
    document_rag_detail: list[DocumentRagDetail] | None
