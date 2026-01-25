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

from src.app.validators.message_schema import InsertNewMessage
from src.config.supabase import get_supabase, init_supabase


async def main():
    await init_supabase()
    db = get_supabase()

    result = (
        await db.table("Conversations")
        .select("*, Customers(name)")
        .eq("business_id", 3)
        .execute()
    )

    if len(result.data) == 0:
        return None

    list_conversations = []

    for i in result.data:
        i["username"] = i["Customers"]["name"]
        del i["Customers"]
        list_conversations.append(i)

    print(list_conversations)


asyncio.run(main())


# from src.infrastructure.vectorstore.chroma_db import rag_system

# rag_system.initial_collection("agent_3")

# document_list = rag_system.list_documents()

# print(document_list)
