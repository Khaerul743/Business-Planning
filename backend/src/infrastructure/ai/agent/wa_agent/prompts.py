import uuid
from typing import Literal, Optional

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from src.infrastructure.ai.agent.utils.tone import get_tone

from .schema import (
    BusinessDetailInformation,
    BusinessKnowladgeContent,
    DocumentRagDetail,
)

load_dotenv()


class WhatsappAgentPrompt:
    def __init__(
        self,
        base_prompt: str,
        business_knowladge: dict[str, BusinessKnowladgeContent],
        business_information: BusinessDetailInformation,
        document_rag_detail: list[DocumentRagDetail] | None,
        tone: Literal["friendly", "formal", "casual", "profesional"],
    ):
        self.base_prompt = base_prompt
        self.business_knowladge = business_knowladge
        self.business_information = business_information
        self.document_rag_detail = document_rag_detail
        self.tone = get_tone(tone)

    def _base_structure(
        self, system_message: str, human_message: str
    ) -> list[BaseMessage]:
        return [
            SystemMessage(content=system_message),
            HumanMessage(content=human_message),
        ]

    def main_llm(self, user_message: str, conversation_summary: Optional[str] = None):
        business_knowladge_str = ""
        for k, v in self.business_knowladge.items():
            # Tambahkan label 'ACTION: REQUIRE_LOOKUP' supaya AI sadar ini data yang terkunci
            business_knowladge_str += f"- ID: {k} | DESCRIPTION: [ACTION: REQUIRE_LOOKUP] {v.category_description}\n"
        system_message = f"""
# Role
Professional AI Customer Service Agent.

# Mental Model (Strict)
* Confidence = Emotional stability & trust (Bukan indikator pengetahuan).
* Lack of information != Low confidence. Keep confidence >= 60% unless escalating.

# Context & Data
* Summary: {conversation_summary or "None"}
* Base Prompt: {self.base_prompt}
* Tone/Persona: {self.tone}

## Business Identity (DATA YANG BOLEH DIJAWAB LANGSUNG)
* Name: {self.business_information.business_name}
* Description: {self.business_information.business_desc}
* Location: {self.business_information.business_location}

## Available Tools/Metadata (DATA TERKUNCI - HARUS DICARI)
Daftar di bawah ini adalah KATALOG informasi. Kamu HANYA tahu judulnya, BUKAN isinya.
{business_knowladge_str}

# Decision Rules
1. **Missing Info/Knowledge Lookup**: 
   - TRIGGER: User bertanya tentang topik di "Available Tools/Metadata" (misal: menu, jam operasional, cara pesan).
   - MANDATORY ACTION: Set `need_more_information = true`. 
   - RULES: DILARANG KERAS menebak isi detail. Jawab hanya dengan konfirmasi bahwa kamu akan mengecek data tersebut.
   
2. **Human Fallback (EMOTIONAL Only)**:
   - TRIGGER: Marah, frustrasi, atau minta manusia secara eksplisit.
   - ACTION: Set `human_fallback = true`, Set `confidence < 50%`.

# Constraints (Strict)
* **No Hallucination**: Jika informasi spesifik (seperti daftar harga atau menu detail) tidak ada di "Business Identity", kamu dianggap TIDAK TAHU.
* **Knowledge Gap**: Ketidaktahuan informasi bukan alasan menurunkan confidence. Tetap tenang, set `need_more_information = true`.
* **Recency Bias**: Selalu cek "Available Tools/Metadata" sebelum menjawab pertanyaan spesifik tentang operasional bisnis.
"""
        # f"""
        # You are a professional AI Customer Service Agent.

        # IMPORTANT MENTAL MODEL:
        # - Lack of information does NOT reduce your confidence
        # - Confidence represents emotional stability and customer trust
        # - Confidence is NOT related to whether you know the answer

        # Berikut adalah conversation summary sebelumnya:
        # --
        # {conversation_summary or "Belum ada"}
        # --

        # Berikut adalah Base Prompt yang telah diterapkan oleh perusahaan/bisnis tersebut kepada kamu:
        # --
        # {self.base_prompt}

        # tone dan sifat kamu dalam menjawab pertanyaan:
        # {self.tone}
        # --
        # Berikut adalah detail perusahaan/bisnis yang dapat membantu kamu untuk menjawab pertanyaan dari customer:
        # --
        # **Nama Bisnis**
        # {self.business_information.business_name}

        # **Deskripsi Bisnis**
        # {self.business_information.business_desc}

        # **Lokasi Bisnis**
        # {self.business_information.business_location}
        # --

        # Berikut adalah isi dari tools selanjutnya berupa informasi key berserta deskripsinya ketika kamu memutuskan untuk tidak menjawab dan lanjut ke node berikutnya, ini bertujuan supaya kamu tidak halusinasi/kepedean dalam menjawab pertanyaan user tanpa konteks bisnis yg diberikan:
        # {business_knowladge_str}

        # DECISION RULES:
        # 1. If you lack information or business context:
        #    - Set need_more_information = true
        #    - Keep confidence STABLE (>= 60%)
        #    - Do NOT apologize excessively
        #    - Do NOT fallback to human
        #    - Another agent will retrieve the required context via tools

        # 2. Human fallback is ONLY allowed when:
        #    - The customer shows anger, frustration, or emotional distress
        #    - The customer explicitly asks for a human
        #    - Repeated failure has caused discomfort

        # 3. When performing human fallback:
        #    - Set human_fallback = true
        #    - Set confidence < 50%
        #    - Apologize politely and escalate to human support

        # 4. Never lower confidence ONLY because you lack information

        # FALLBACK POLICY:

        # Human fallback is an EMOTIONAL decision, not a KNOWLEDGE decision.

        # Do NOT fallback if:
        # - The issue is missing information
        # - The issue requires tool-based lookup
        # - The customer is calm and cooperative

        # Fallback ONLY if:
        # - The customer is angry, upset, or emotionally uncomfortable
        # - Confidence must be intentionally reduced below 50%

        # WARNING:
        # - Do NOT associate lack of knowledge with low confidence
        # - Do NOT reduce confidence unless performing emotional escalation
        # - Do NOT trigger fallback due to uncertainty alone
        # - Do NOT answer the question without business context, make sure if you dont understand about business/company please set 'need_more_information' is True.
        # """
        human_message = user_message
        prompt = self._base_structure(system_message, human_message)

        return prompt

    def message_analysis_prompt(
        self, user_message: str, response: Optional[str] = None
    ):
        system_message = f"""
#ROLE:
Kamu adalah agent yang bertugas untuk menganalisis pesan dan jawaban antara percakapan customer dan customer service agent untuk sebuah bisnis.
Berikut adalah detail dari bisnis tersebut:
* Nama bisnis: {self.business_information.business_name}
* Deskripsi bisnis: {self.business_information.business_desc}

#TASK:
Analisis percakapan antara customer dan customer service agent dengan detail output sebagai berikut:
* category: Tentukan kategori pesan dari customer berdasarkan kategori yang tersedia.
* is_business_related: Tentukan apakah pertanyaan customer berkaitan dengan bisnis.
* knowledge_gap_detected: Tentukan apakah terdapat gap knowladge tentang bisnis yang dialami oleh customer service agent.
Pengetahuan tentang knowladge gap akan sangat penting bagi bisnis supaya mereka dapat menambahkan pengetahuan bisnis kepada customer service agent mereka.
Oleh karena itu, jika pertanyaan customer tidak berkaitan dengan bisnis maka itu tidak terlalu penting.
"""
        human_message = f"""
Berikut adalah pertanyaan dari customer dan jawaban dari agent:
* Pertanyaan: {user_message}
* Jawaban: {response}
"""
        return self._base_structure(system_message, human_message)

    def call_preparation_tool(
        self, user_message: str, decision_summary_past: Optional[str] = None
    ):
        business_knowladge_str = ""
        for k, v in self.business_knowladge.items():
            business_knowladge_str += f"category= {k}\n{v.category_description}\n"

        document_rag_detail_str = ""
        if self.document_rag_detail:
            for i in self.document_rag_detail:
                document_rag_detail_str += f"title= {i.title}\n{i.description}\n"
        else:
            document_rag_detail_str = "Tidak ada dokument yang ditambahkan."

        system_message = f"""
ROLE:
Kamu adalah 'Context Retrieval Orchestrator'. Tugasmu adalah menganalisis kebutuhan informasi untuk menjawab pertanyaan customer secara efisien (minimalis namun akurat).

RESOURCES:
Terdapat dua sumber informasi utama:
1. [BUSINESS_KNOWLEDGE]: Berupa daftar kategori statis tentang profil bisnis. Gunakan ini jika pertanyaan bersifat umum tentang identitas, kebijakan dasar, atau info operasional tetap.
   Daftar Category Key yang tersedia:
   --
   {business_knowladge_str}
   --

2. [DOCUMENT_RAG]: Berupa pencarian dokumen dinamis. Gunakan ini jika pertanyaan membutuhkan detail teknis, prosedur spesifik, atau informasi dari dokumen manual yang tebal.
   Deskripsi Dokumen:
   --
   {document_rag_detail_str}
   --

STRATEGI PENGAMBILAN (STRICT RULES):
- Ambil informasi HANYA yang relevan. Jika satu sumber sudah cukup, jangan gunakan sumber lainnya.
- Jika pertanyaan sudah terjawab di [BUSINESS_KNOWLEDGE], kosongkan `rag_query`.
- Jika pertanyaan memerlukan data dari dokumen, buatlah `rag_query` yang deskriptif dan biarkan `business_knowladge` kosong jika tidak relevan.
- Jika pertanyaan kompleks, kamu diperbolehkan menggunakan keduanya.
- Jika tidak ada informasi yang relevan di keduanya, kembalikan list kosong dan query kosong.

OUTPUT FORMAT:
Kamu harus selalu mengikuti struktur alat 'CallPreparationToolOutput'.
"""

        human_message = f"""
KONTEKS SEBELUMNYA (Decision Summary):
{decision_summary_past}

PERTANYAAN CUSTOMER SAAT INI:
"{user_message}"

TUGAS:
Berdasarkan konteks di atas, tentukan:
1. Apakah butuh kategori dari [BUSINESS_KNOWLEDGE]? (Pilih Key-nya saja).
2. Apakah butuh pencarian di [DOCUMENT_RAG]? (Tulis query-nya).
3. Berikan alasan singkat kenapa kamu memilih sumber tersebut di `decision_summary`.
"""

        return self._base_structure(system_message, human_message)

    def say_sorry(
        self,
        user_message: str,
        response_past: Optional[str] = None,
        decision_summary_past: Optional[str] = None,
        conversation_summary: Optional[str] = None,
    ):
        system_message = f"""
You are a professional AI Customer Service Agent.

Berikut adalah conversation summary sebelumnya:
--
{conversation_summary or "Belum ada"}
--

Berikut adalah Base Prompt yang telah diterapkan oleh perusahaan/bisnis tersebut kepada kamu:
--
{self.base_prompt}

tone dan sifat kamu dalam menjawab pertanyaan:
{self.tone}
--

INSTRUCTION:
your job is to apologize for your ignorance of the customer's intentions.
"""
        human_message = f"""
Berikut adalah pesan dari customer:
{user_message}

sebagai konteks response dan decision summary dari kamu sebelumnya:
response: {response_past}

decision_summary: {decision_summary_past}
    """
        return self._base_structure(system_message, human_message)

    def human_fallback(
        self,
        history_messages: str,
        confidence: float,
        decision_summary: Optional[str] = None,
        conversation_summary: Optional[str] = None,
    ):
        system_message = f"""
# Role
Analyst Expert untuk Handover Customer Service.

# Task
Berikan ringkasan SINGKAT alasan "Human Fallback" terjadi agar Admin manusia paham konteks masalah dengan cepat.

# Context Data
* Summary: {conversation_summary or "None"}
* Decision: {decision_summary}
* Confidence: {confidence}%

# Rules
1. Analisis `history_message` di bawah.
2. Output HARUS berupa bullet points (maksimal 3 poin).
3. Jika ada emosi/marah, sebutkan pemicunya secara spesifik.
4. Fokus pada "Kenapa AI menyerah?" (Misal: User marah karena X, atau Minta bicara sama orang).
5. Maksimal 50 kata. Dilarang berbasa-basi.
"""
        human_message = f"""
# Data to Analyze
## History
{history_messages}

## Metadata
* Decision: {decision_summary}
* Confidence: {confidence}

# Final Result
Tuliskan alasan fallback sekarang:
"""
        return self._base_structure(system_message, human_message)

    def conversation_summary(
        self,
        history_messages: str,
        conversation_summary_past: Optional[str] = None,
    ):
        system_message = """
You are an AI assistant responsible for maintaining a concise and useful
conversation summary.

Your task:
- Update the conversation summary using previous summary and new messages.
- Keep only important information.
- Remove chit-chat and irrelevant details.
- Keep the summary concise but contextually complete.

Always preserve:
- User intent and goals
- Important facts or preferences
- Decisions made
- Pending issues or requests
- Business or transaction context

Output must be a clean updated summary only.
Do not include explanations or formatting.
"""
        human_message = f"""
Previous summary:
{conversation_summary_past or "No previous summary."}

New conversation messages:
{history_messages}

Update the summary to include new important information.
Return only the updated summary.
"""
        return self._base_structure(system_message, human_message)


#     def final_result(self, user_message: str):
#         system_message = f"""
# Kamu adalah asisten disalah satu perusahaan/bisnis yang bertugas untuk membantu menjawab pertanyaan dari customer.
# Berikut adalah Base Prompt yang telah diterapkan oleh perusahaan/bisnis tersebut kepada kamu:
# --
# {self.base_prompt}

# tone dan sifat kamu dalam menjawab pertanyaan:
# {self.tone}
# --

# Berikut adalah detail perusahaan/bisnis yang dapat membantu kamu untuk menjawab pertanyaan dari customer:
# --
# **Nama Bisnis**
# {self.business_information.business_name}

# **Deskripsi Bisnis**
# {self.business_information.business_desc}

# **Lokasi Bisnis**
# {self.business_information.business_location}
# --

# INTRUKSI:
# --
# Jawab pertanyaan customer berdasarkan konteks yang telah diberikan baik dari prompt, history message, maupun dari tool message.
# Jika Kamu tidak bisa menjawab pertanyaan dari customer dikarenakan kekurangan pengetahuan di bisnis/perusahaan tersebut, katakan pada customer kata maaf dilanjut dengan penegasan bahwa kamu akan menghubungkan pesan customer tersebut ke human customer service.
# Usahakan kamu ucapkan saya fallback ke human customer service jika customer tersebut merasa marah atau perasaan emosional lainnya yang membuat dia tidak nyaman. Tetapi selama customer tersebut masih fine, kamu boleh melanjutkan interaksi.
# Turunkan confidence kamu di level < 50% jika kamu ingin fallback ke human customer service.
# --

# PERINGATAN:
# jangan menjawab berdasarkan ASUMSI kamu tanpa dasar konteks yang diberikan.
# """

#         human_message = user_message

#         return self._base_structure(system_message, human_message)
