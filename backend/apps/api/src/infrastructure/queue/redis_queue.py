import json
from typing import Optional
from redis import Redis


class RedisQueue:
    def __init__(self, redis_client: Redis, queue_name: str):
        self.redis_client = redis_client
        self.queue_name = queue_name

    def enqueue(self, data: dict):
        payload = json.dumps(data)
        self.redis_client.lpush(self.queue_name, payload)

    def dequeue(self, timeout: int = 0) -> Optional[dict]:
        result = self.redis_client.brpop(self.queue_name, timeout)
        if result:
            _, payload = result
            return json.loads(payload)
        return None
