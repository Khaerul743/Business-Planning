import asyncio

from src.config.supabase import get_supabase, init_supabase
from src.domain.models.business_knowladges import BusinessKnowladge


async def main():
    await init_supabase()
    db = get_supabase()

    result = (
        await db.table("Business_knowladges")
        .delete()
        .eq("id", 3)
        .eq("business_id", 3)
        .execute()
    )
    print(result)
    print(result.count)


asyncio.run(main())
