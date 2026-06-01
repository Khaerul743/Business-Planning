import asyncio
from dotenv import load_dotenv
import os
from supabase import create_async_client

load_dotenv()

async def main():
    url = os.environ.get("SUPABASE_URL", "http://localhost:8000")
    key = os.environ.get("SUPABASE_SERVICE_KEY", "dummy")
    client = await create_async_client(url, key)
    print("Client created successfully:", client)

asyncio.run(main())
