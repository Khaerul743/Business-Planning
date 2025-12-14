import asyncio

from src.config.supabase import get_supabase, init_supabase
from src.domain.repositories import UserRepository


async def main():
    await init_supabase()
    db = get_supabase()
    user = UserRepository(db)

    result = await user.get_user_by_id(1)
    print(result)


asyncio.run(main())
