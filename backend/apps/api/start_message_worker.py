import asyncio
from src.infrastructure.queue import (
    RedisQueue,
    RedisLock,
    Worker,
    JobDispatcher,
)
from src.config.supabase import init_supabase, get_supabase
from src.infrastructure.queue.handler import (
    InvokeAgentHandler,
)
from src.infrastructure.queue.redis import redis_client

message_queue = RedisQueue(redis_client, "message_queue")

lock = RedisLock(redis_client)


async def main():
    # init async resource
    await init_supabase()

    db = get_supabase()

    message_dispatcher = JobDispatcher()

    # Regis handler
    message_dispatcher.register("invoke_agent", InvokeAgentHandler(db))

    message_worker = Worker(message_queue, lock, message_dispatcher)

    # Buat file worker baru mas
    await message_worker.start()


if __name__ == "__main__":
    asyncio.run(main())
