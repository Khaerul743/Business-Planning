import asyncio
from src.infrastructure.queue import (
    RedisQueue,
    RedisLock,
    Worker,
    JobDispatcher,
)
from src.config.supabase import init_supabase, get_supabase
from src.infrastructure.queue.handler import (
    GenerateInsightHandler,
    GenerateGapKnowladgeHandler,
)
from src.infrastructure.queue.redis import redis_client

generator_queue = RedisQueue(redis_client, "generator_queue")

lock = RedisLock(redis_client)


async def main():
    # init async resource
    await init_supabase()

    db = get_supabase()

    generator_dispatcher = JobDispatcher()

    # Regis handler
    generator_dispatcher.register("generate_insight", GenerateInsightHandler(db))
    generator_dispatcher.register(
        "generate_gap_knowladge", GenerateGapKnowladgeHandler(db)
    )

    generator_worker = Worker(generator_queue, lock, generator_dispatcher)

    # Buat file worker baru mas
    await generator_worker.start()


if __name__ == "__main__":
    asyncio.run(main())
