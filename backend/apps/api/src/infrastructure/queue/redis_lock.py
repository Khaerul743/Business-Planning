from redis import Redis


class RedisLock:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    def acquire(self, key: str, expire: int = 30):
        return self.redis_client.set(key, "1", nx=True, ex=expire)

    def release(self, key: str):
        self.redis_client.delete(key)
