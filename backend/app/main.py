from fastapi import FastAPI
from app.settings import settings
from app.db import check_db
from app.redis_client import check_redis

app = FastAPI(title="Pokemon Stadium")

# liveness probe
@app.get("/health")
def health():
  return {"ok": True}

# readiness probe
@app.get("/ready")
def ready():
  # "ready" should check dependencies
  check_db()
  check_status()
  return {"ok": True}
