from uuid import UUID
import asyncio
from src.repositories.knowladge_repository import KnowladgeRepository
from src.config.supabase import init_supabase, get_supabase
from src.whatsapp_agent.utils.business_context_manager import BusinessContextManager


async def main():
    await init_supabase()
    db = get_supabase()
    bc = BusinessContextManager(db)
    result = await bc.get_context(
        UUID("a04b8eb2-3b32-44e2-9a6a-bbca2c23ab58"),
        UUID("06a8a34c-12f8-42c6-bf09-33f2e3a08171"),
    )
    print(result)


asyncio.run(main())
