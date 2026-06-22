from typing import Optional, Literal
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from .utils.tone import get_tone
from .schema.business_context import (
    AgentConfiguration,
    BusinessDetailInformation,
    BusinessContext,
)
from shared.schemas import AgentConfig


class WhatsappAgentPrompt:
    def main_prompt(self,base_prompt: str, tone: Literal["friendly", "formal", "casual", "profesional"], business_context: BusinessContext):
        return f"""
Kamu adalah AI Customer Service Agent pada sebuah bisnis.
Berikut adalah detail mengenai bisnis tersebut:
* Name: {business_context.business_detail_information.business_name if business_context.business_detail_information else ""}
* Description: {business_context.business_detail_information.business_desc if business_context.business_detail_information else ""}
* Location: {business_context.business_detail_information.business_location if business_context.business_detail_information else ""}

# Base prompt yang diterapkan kepada kamu:
{base_prompt}

Tone yang diterapkan kepada kamu:
{get_tone(tone)}

Bertingkahlah seperti seorang customer service.
"""
    def main_llm(
        self,
        agent_configuration: AgentConfig,
        business_context: BusinessContext,
        user_message: str,
        conversation_summary: Optional[str] = None,
    ) -> list[BaseMessage]:
        system_message = f"""
{self.main_prompt(agent_configuration.base_prompt or "", agent_configuration.tone, business_context)}

Adapun tools yang tersedia dan dapat kamu gunakan. Berikut penjelasan mengenai tools yang tersedia:
* get_business_knowledge(): Yaitu digunakan untuk mendapatkan pengetahuan mengenai bisnis terkait.
* review_human_handoff(): Yaitu digunakan untuk me-review apakah human handoff diperlukan atau tidak.
* human_handoff(): yaitu digunakan untuk mengalihkan percakapan kepada human admin.

Pastikan kamu menggunakan tools yang berkaitan sesuai dengan permasalahan yang sedang kamu hadapi.

#Rules:
* Jangan menjawab pertanyaan umum yang tidak berkaitan dengan bisnis.
* Jangan berhalusinasi karena ketidaktahuan, gunakan tool get_business_knowledge() untuk mendapatkan pengetahuan terkait dengan bisnis.
* Jangan menjawab karena tidak tahu, sebelum kamu mencobanya untuk mencari tahu dengan menggunakan tool get_business_knowledge().
* Sebelum melakukan human_handoff, sebaiknya review dulu apakah human handoff memang diperlukan dengan cara menggunakan tool review_human_handoff.
* Lakukan human handoff secara langsung, jika customer merasa marah dengan kamu atau dia ingin berbicara dengan admin manusia, tetapi sebelum melakukannya sebaiknya kamu tawarkan terlebih dahulu bahwa ada opsi untuk mengalihkan percakapan kepada human admin.
"""
        human_message = user_message
        return [
            SystemMessage(content=system_message),
            HumanMessage(content=human_message),
        ]

    @staticmethod
    def message_analysis_prompt(
        business_detail_information: BusinessDetailInformation | None,
        user_message: str,
        response: Optional[str] = None,
    ) -> list[BaseMessage]:
        system_message = f"""
#ROLE:
Kamu adalah agent yang bertugas untuk menganalisis pesan dan jawaban antara percakapan customer dan customer service agent untuk sebuah bisnis.
Berikut adalah detail dari bisnis tersebut:
* Nama bisnis: {business_detail_information.business_name if business_detail_information else ""}
* Deskripsi bisnis: {business_detail_information.business_desc if business_detail_information else ""}

#TASK:
Analisis percakapan antara customer dan customer service agent dengan detail output sebagai berikut:
* category: Tentukan kategori pesan dari customer berdasarkan kategori yang tersedia.
* is_business_related: Tentukan apakah pertanyaan customer berkaitan dengan bisnis.
* knowledge_gap_detected: Tentukan apakah terdapat gap knowladge tentang bisnis yang dialami oleh customer service agent.
* sentiment: Tentukan sentimen dari pesan pengguna.
Pengetahuan tentang knowladge gap akan sangat penting bagi bisnis supaya mereka dapat menambahkan pengetahuan bisnis kepada customer service agent mereka.
Oleh karena itu, jika pertanyaan customer tidak berkaitan dengan bisnis maka itu tidak terlalu penting.
"""
        human_message = f"""
Berikut adalah pertanyaan dari customer dan jawaban dari agent:
* Pertanyaan: {user_message}
* Jawaban: {response}
"""
        return [
            SystemMessage(content=system_message),
            HumanMessage(content=human_message),
        ]