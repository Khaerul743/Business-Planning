from redis import Redis
from dotenv import load_dotenv
from src.config.setting import settings

load_dotenv()

redis_host = settings.REDIS_HOST
redis_port = settings.REDIS_PORT

redis_client = Redis(host=redis_host, port=redis_port)
