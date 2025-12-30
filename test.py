import asyncio

from src.config.supabase import get_supabase, init_supabase
from src.domain.models.business_knowladges import BusinessKnowladge


async def main():
    await init_supabase()
    db = get_supabase()

    result = (
        await db.table("Businesses")
        .select("id")
        .eq("user_id", 4)
        .maybe_single()
        .execute()
    )

    print(result.data["id"])


asyncio.run(main())
