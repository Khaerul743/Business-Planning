from dotenv import load_dotenv
from supabase import AsyncClient, create_async_client

from src.core.exceptions import SupabaseMissingParameter

from .setting import settings

load_dotenv()
supabase: AsyncClient | None = None


async def init_supabase():
    global supabase
    supabase_url = settings.SUPABASE_URL
    supabase_service_key = settings.SUPABASE_SERVICE_KEY
    if not supabase_url or not supabase_service_key:
        raise SupabaseMissingParameter()
    supabase = await create_async_client(supabase_url, supabase_service_key)


def get_supabase() -> AsyncClient:
    if supabase is None:
        raise RuntimeError("Supabase client not initialized")
    return supabase
