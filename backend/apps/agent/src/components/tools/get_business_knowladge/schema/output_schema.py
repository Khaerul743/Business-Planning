from typing import Literal, Optional, List
from pydantic import create_model, Field, BaseModel

def create_gathering_knowledge_output(business_knowladge: list[str]):
    business_knowladge_type = Literal[tuple(business_knowladge)]
    return create_model(
        "CallPreparationToolOutput",
        rag_query=(
            Optional[str],  # Gunakan Optional
            Field(
                default="",  # Kasih default string kosong
                description="Query untuk RAG. Isi hanya jika butuh mencari di dokumen. Kosongkan jika tidak butuh.",
            ),
        ),
        business_knowladge=(
            List[business_knowladge_type],
            Field(
                default_factory=list,  # Default list kosong
                description="List category key. Isi hanya yang relevan. Kosongkan jika tidak ada yang cocok.",
            ),
        ),
        decision_summary=(
            str,
            Field(
                description=(
                    "Ringkasan reasoning"
                    "Jelaskan apa yang sudah kamu lakukan dan mengapa"
                )
            ),
        ),
        __base__= BaseModel,
    )