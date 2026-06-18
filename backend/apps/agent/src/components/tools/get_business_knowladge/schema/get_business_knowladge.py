from pydantic import BaseModel, Field


class BusinessKnowladgeInput(BaseModel):
    query: str = Field(description="Kata kunci untuk mengakses informasi yang relevan")
    conversation_context: str = Field(description="Berikan konteks terkait dengan conversation yang sedang dilakukan")
    decision_summary: str = Field(description="Ringkasan dari keputusan yang kamu lakukan")

