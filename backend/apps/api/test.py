# from src.app.validators.agent_schema import WhatsappAgentConfig
# from src.infrastructure.ai.agent.manager import WhatsappAgentManager

# manager = WhatsappAgentManager()

# agent_conf = WhatsappAgentConfig(
#     chromadb_path="chromadb",
#     collection_name="my_collection",
#     llm_provider="openai",
#     llm_model="gpt-3.5-turbo",
#     tone="casual",
#     base_prompt="",
# )

# agent = manager.get_or_create(1, agent_conf)

# print(agent.get_llm_model())


import asyncio
from datetime import datetime
from uuid import UUID

# from src.app.validators.message_schema import InsertNewMessage
from apps.api.src.config.supabase import get_supabase, init_supabase

# from src.domain.models import Human_Fallback


async def main():
    await init_supabase()
    db = get_supabase()

    result = (
        await db.table("Businesses")
        .select("id, Agents(id)")
        .eq("user_id", "95050121-195f-4783-98f7-9e24b94f7cd3")
        .maybe_single()
        .execute()
    )

    print(result.data)


asyncio.run(main())


# from src.infrastructure.vectorstore.chroma_db import rag_system

# rag_system.initial_collection("agent_3")

# document_list = rag_system.list_documents()

# print(document_list)

# from typing import Sequence

# from src.infrastructure.ai.agent.wa_agent import (
#     BusinessDetailInformation,
#     WhatsappAgent,
#     WhatsappAgentState,
# )

# business_inf = BusinessDetailInformation(
#     business_name="Rusdi store",
#     business_desc="Merupakan salah satu online store paling laris di ngawi selatan",
#     business_location="Ngawi selatan, kec. Rongawi, kab. Rongawi Kuno",
# )

# bk = {
#     "owner": {"description": "untuk mengetahui nama owner", "content": "rusdi"},
#     "product": {
#         "description": "product yang tersedia di rusdi barber",
#         "content": "- Gatsby pomade by amba\n- shampo muani maknyus\n- Minyak rambut khas bumi ayu",
#     },
# }
# agent = WhatsappAgent(
#     "chromadb", "default", "gpt-4o-mini", "openai", "", "formal", business_inf, bk
# )

# print(agent.get_response())
# while True:
#     input_user = input("user: ")
#     if input_user == "stop":
#         break
#     result = agent.execute(
#         WhatsappAgentState(
#             user_message=input_user,
#             need_more_information=False,
#             messages=[],
#         ),
#         "default",
#     )
#     if input_user == "state":
#         print(result)
#         break

#     print(agent.get_response());
# from src.infrastructure.ai.agent.agent_analysis_gap import (
#     AgentAnalysisGapState,
#     AgentAnalysisGap,
# )

# business_desc = "Ayam Bakar Naufal adalah usaha kuliner rumahan yang menyajikan berbagai menu ayam bakar dengan bumbu khas nusantara. Selain ayam bakar, tersedia juga beberapa pilihan lauk pendamping seperti ayam goreng, ikan bakar, dan aneka sambal. "
# raw_data = [
#     {
#         "ai_response": "Saya belum menemukan informasi tentang promo yang tersedia di Ayam Bakar Naufal. Kamu bisa cek langsung ke tempat atau tanya di media sosial mereka untuk info lebih lanjut!",
#         "user_message": "apakah ada promo?",
#         "category": "promo",
#         "is_business_related": True,
#         "knowledge_gap_detected": True,
#     }
# ]

# agent = AgentAnalysisGap()
# result = agent.execute(
#     AgentAnalysisGapState(
#         messages=[],
#         user_message="",
#         business_description=business_desc,
#         raw_data=raw_data,
#     ),
#     "default",
# )

# print(result)
# from redis import Redis
# from src.infrastructure.queue import RedisQueue

# redis = Redis(host="localhost", port=6379)

# queue = RedisQueue(redis, "test_qeueu")

# queue.enqueue(
#     {
#         "queue_id": "121233",
#         "type": "test_job",
#         "retry": 0,
#         "job_payload": {
#             "user_message": "rusdi",
#             "phone_number_id": "123",
#             "customer_data": {"wa_id": "02899239"},
#         },
#     }
# )

# queue.enqueue(
#     {
#         "queue_id": "121233",
#         "type": "test_job",
#         "retry": 0,
#         "job_payload": {
#             "user_message": "imut",
#             "phone_number_id": "123",
#             "customer_data": {"wa_id": "02899239"},
#         },
#     }
# )
