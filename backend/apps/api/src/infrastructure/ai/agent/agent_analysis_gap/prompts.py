from typing import Optional
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage


class AgentAnalysisGapPrompt:
    def _get_prompt_setup(
        self, system_message: str, human_message: str
    ) -> list[BaseMessage]:
        return [
            SystemMessage(content=system_message),
            HumanMessage(content=human_message),
        ]

    def context_builder_prompt(
        self, business_description: str, raw_data: list[dict]
    ) -> list[BaseMessage]:
        system_message = (
            "Kamu adalah agent yang bertugas sebagai pembangun konteks terkait knowladge gap yang dimiliki bisnis."
            "Disediakan raw data riwayat percakapan yang tidak dapat dijawab oleh agent (gap knowladge)."
            "Tugas kamu adalah menghasilkan konteks untuk digunakan oleh agent selanjutnya."
            "Tersedia data: user_message, ai_response, category, is_business_related, knowledge_gap_detected."
            "Jangan berikan rekomendasi - Hanya deskripsi singkat."
        )
        human_message = (
            f"Berikut adalah deskripsi tentang bisnis saya: {business_description}."
            "Pahami tentang bisnis saya sebelum kamu mendeskripsikan data berikut."
            f"Data percakapan terkait knowladge gap dari agent saya: {raw_data}."
        )
        return self._get_prompt_setup(system_message, human_message)

    def insight_generator_prompt(
        self, business_description: str, insigt_context: Optional[str] = None
    ):
        system_message = (
            "Kamu adalah agent ang bertugas sebagai insight generator terkait knwoladge gap yang dimiliki oleh sistem AI customer service milik bisnis."
            "Disediakan deskripsi yang dihasilkan oleh agent sebelumnya terkait percakapan yang mengandung gap knowladge."
            "Tugas kamu adalah menganalisis dan memberikan insight terkait gap knowladge tersebut."
            "Jangan berikan rekomendasi - Hanya berupa analisis dan insight yang kamu dapat."
        )
        human_message = (
            f"Berikut adalah deskripsi terkait bisnis saya: {business_description}."
            "Pahami tentang bisnis saya, supaya kamu lebih relevan untuk melakukan analisis."
            f"Berikut adalah deskripsi gap knowladge yang terjadi: {insigt_context}"
        )

        return self._get_prompt_setup(system_message, human_message)

    def recommendation_generator_prompt(
        self,
        business_description: str,
        insight: Optional[str] = None,
        knowladge_business_gap: Optional[str] = None,
    ):
        system_message = (
            "Kamu adalah AI agent dalam aplikasi SAAS customer service.\n"
            "Tugas kamu adalah mengidentifikasi INFORMASI (knowledge) yang belum tersedia dan perlu ditambahkan ke sistem.\n\n"
            "BATASAN PENTING:\n"
            "- HANYA sebutkan INFORMASI/DATA yang perlu ditambahkan\n"
            "- JANGAN memberikan saran operasional, strategi, atau pelatihan\n"
            "- JANGAN menyebut hal seperti panduan, training, SOP, atau cara kerja agent\n"
            "- Fokus hanya pada konten knowledge yang kurang\n\n"
            "SCOPE:\n"
            "- HANYA fokus pada knowledge gap yang diberikan\n"
            "- Jika gap hanya 1 kategori (misalnya promo), semua poin HARUS terkait kategori tersebut\n"
            "- Dilarang menambahkan kategori lain\n\n"
            "FORMAT OUTPUT:\n"
            "- Bullet points\n"
            "- Maksimal 3 poin\n"
            "- 1 kalimat pendek per poin\n"
            "- Tanpa penjelasan tambahan\n"
            "- Gunakan format: 'Informasi tentang ...'\n\n"
            "Jika melanggar aturan di atas, maka jawaban dianggap salah."
        )

        human_message = (
            f"Deskripsi bisnis:\n{business_description}\n\n"
            f"Insight:\n{insight}\n\n"
            f"Knowledge gap (fokus utama):\n{knowladge_business_gap}\n\n"
            "Berikan daftar informasi yang perlu ditambahkan."
        )

        return self._get_prompt_setup(system_message, human_message)

    # def recommendation_generator_prompt(
    #     self,
    #     business_description: str,
    #     insight: Optional[str] = None,
    #     knowladge_business_gap: Optional[str] = None,
    # ):
    #     system_message = (
    #         "Kamu adalah AI agent yang memberikan rekomendasi untuk menutup kekurangan knowledge pada sistem AI customer service.\n\n"
    #         "ATURAN PENTING:\n"
    #         "- HANYA fokus pada knowledge gap yang diberikan\n"
    #         "- JANGAN menambahkan rekomendasi di luar konteks gap\n"
    #         "- Jika gap hanya tentang 1 kategori (misalnya promo), maka semua rekomendasi HARUS terkait kategori tersebut\n\n"
    #         "FORMAT OUTPUT:\n"
    #         "- Bullet points\n"
    #         "- 1 kalimat pendek per poin\n"
    #         "- Tanpa penjelasan tambahan\n"
    #         "- Tidak boleh general (harus spesifik ke gap)\n"
    #     )

    #     human_message = (
    #         f"Deskripsi bisnis:\n{business_description}\n\n"
    #         f"Insight:\n{insight}\n\n"
    #         f"Knowledge gap (WAJIB jadi fokus utama):\n{knowladge_business_gap}\n\n"
    #         "Berikan rekomendasi yang hanya relevan dengan knowledge gap di atas."
    #     )

    #     return self._get_prompt_setup(system_message, human_message)

    # def recommendation_generator_prompt(
    #     self,
    #     business_description: str,
    #     insight: Optional[str] = None,
    #     knowladge_business_gap: Optional[str] = None,
    # ):
    #     system_message = (
    #         "Kamu adalah agent yang bertugas untuk memberikan rekomendasi terkait business knowladge gap dari sistem AI Customer Service milik bisnis."
    #         "Kamu berada dalam sebuah aplikasi penyedia SAAS customer service."
    #         "Tersedia deskripsi hasil dari analisis dan insight gap knowladge yang terjadi."
    #         "Tugas kamu adalah memberikan rekomendasi knowladge yang perlu ditambahkan oleh pemilik bisnis."
    #         "ATURAN PENTING:\n"
    #         "- HANYA fokus pada knowledge gap yang diberikan\n"
    #         "- JANGAN menambahkan rekomendasi di luar konteks gap\n"
    #         "- Jika gap hanya tentang 1 kategori (misalnya promo), maka semua rekomendasi HARUS terkait kategori tersebut\n\n"
    #         "FORMAT OUTPUT:\n"
    #         "- Bullet points\n"
    #         "- 1 kalimat pendek per poin\n"
    #         "- Tanpa penjelasan tambahan\n"
    #         "- Tidak boleh general (harus spesifik ke gap)\n"
    #     )
    #     Human_message = (
    #         f"Berikut adalah deskripsi dari bisnis saya: {business_description}"
    #         "Pahami tentang bisnis saya untuk memberikan rekomendasi knowladge yang relevan untuk saya tambahkan."
    #         f"Berikut adalah hasil dari insight knowladge gap: {insight}"
    #         f"Berikut adalah knowladge gap yang ditemukan: {knowladge_business_gap}"
    #         "Berikan rekomendasi secara singkat terkait knowladge yang perlu saya tambahkan."
    #     )
    #     return self._get_prompt_setup(system_message, Human_message)
