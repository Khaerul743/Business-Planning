import asyncio
from .redis_queue import RedisQueue
from .redis_lock import RedisLock
from .dispatcher import JobDispatcher
from .job_models import BaseJob


class Worker:
    def __init__(self, queue: RedisQueue, lock: RedisLock, dispatcher: JobDispatcher):
        self.queue = queue
        self.lock = lock
        self.dispatcher = dispatcher

    def get_lock_key(self, job: BaseJob):
        payload = job.job_payload
        if job.type == "invoke_agent":
            return (
                f"lock:{payload['phone_number_id']}:{payload['customer_data']['wa_id']}"
            )

        return None

    async def requeue_with_retry(self, job: BaseJob):
        job.retry += 1

        if job.retry > job.max_retry:
            print(f"[DROP] {job.queue_id}")
            return

        delay = 2**job.retry

        print(f"[RETRY] {job.queue_id} delay={delay}")
        await asyncio.sleep(delay)

        self.queue.enqueue(job.model_dump())

    async def start(self):
        print("Worker started...")
        while True:
            try:
                raw = self.queue.dequeue()
            except Exception as e:
                print(f"[QUEUE ERROR] {e}")
                await asyncio.sleep(1)
                continue

            if not raw:
                await asyncio.sleep(0.1)
                continue

            try:
                job = BaseJob(**raw)
            except Exception as e:
                print(f"[INVALID JOB] {e}")
                continue

            lock_key = self.get_lock_key(job)
            if lock_key:
                if self.lock.acquire(lock_key, expire=60):
                    try:
                        await self.dispatcher.dispatch(job)
                    except Exception as e:
                        print(f"[ERROR] {e}")
                        await self.requeue_with_retry(job)
                    finally:
                        self.lock.release(lock_key)
                else:
                    print("[LOCKED] requeue with retry")
                    await self.requeue_with_retry(job)
            else:
                try:
                    await self.dispatcher.dispatch(job)
                except Exception as e:
                    print(f"[ERROR] {e}")
                    await self.requeue_with_retry(job)
