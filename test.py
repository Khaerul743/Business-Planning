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


# import asyncio

# from src.config.supabase import get_supabase, init_supabase


# async def main():
#     await init_supabase()
#     db = get_supabase()

#     result = (
#         await db.table("Document_knowladges")
#         .select("*")
#         .eq("agent_id", 3)
#         .eq("id", 8)
#         .maybe_single()
#         .execute()
#     )
#     print(result)


# asyncio.run(main())


# from src.infrastructure.vectorstore.chroma_db import rag_system

# rag_system.initial_collection("agent_3")

# document_list = rag_system.list_documents()

# print(document_list)

from src.core.utils.save_file import save_file_handler

save_file_handler.delete_file("documents/user_4/agent_3", "Khaerul_lutfi.pdf")
