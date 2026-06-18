from langchain_core.messages import SystemMessage, HumanMessage
from src.whatsapp_agent.schema.business_context import BusinessContext

class ToolPrompt:
    @staticmethod
    def gathering_knowledge(business_context: BusinessContext, keyword: str, conversation_context: str):
        business_knowladge_str = ""
        if business_context.business_knowladge_content:
            for k, v in business_context.business_knowladge_content.items():
                business_knowladge_str += f"category= {k}\n{v.category_description}\n"
        else:
            business_knowladge_str = "Tidak ada business knowladge yang ditambahkan."
        document_rag_detail_str = ""
        if business_context.document_rag_detail:
            for i in business_context.document_rag_detail:
                document_rag_detail_str += f"title= {i.title}\n{i.description}\n"
        else:
            document_rag_detail_str = "Tidak ada dokument yang ditambahkan."
        
        system_message = f"""
Kamu adalah agent yang ditugaskan untuk mengambil pengetahuan tentang bisnis.
Terdapat dua macam untuk mengambil pengetahuan tersebut yaitu:
* Melalui business knowladge: yaitu pengetahuan yang bisa kamu dapatkan hanya menggunakan category dan dari masing-masing category terdapat deskripsi. Dari deskripsi tersebut kamu bisa menentukan kira-kira category mana yang relevan untuk diambil.
* Melalui document: yaitu berupa dokument tentang bisnis. Kamu bisa mendapatkan pengetahuan tersebut hanya dengan menggunakan query yang relevan.

# Berikut adalah list pengetahuan dari bisnis yang tersedia:
1. Business knowladge:
   --
   {business_knowladge_str}
   --

2. Document knowladge:
   --
   {document_rag_detail_str}
   --

Masing-masing dari pengetahuan tersebut terdapat deskripsi. Deskripsi tersebut bertujuan supaya kamu dapat menentukan untuk mengambil pengetahuan yang relevan saja (tidak harus semuanya).

# Rule:
Apabila dari salah satu pengetahuan tersebut tidak relevan untuk diambil, maka kosongkan saja. Begitu juga jika keduanya tidak relevan.
"""
        human_message = f"""
Tolong bantu saya dalam mengambil pengetahuan tentang bisnis. Berikut adalah kata kunci dan conversation context:
--
{keyword}
--

#Konteks:
{conversation_context}

"""
        return [system_message, human_message]