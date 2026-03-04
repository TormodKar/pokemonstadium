import redis 
from app.settings import settings

_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)

def check_redis() -> None:
  _client.ping()
  _client.set("poke:ping", "1", ex=10)
  assert _client.get("poke:ping") == "1"