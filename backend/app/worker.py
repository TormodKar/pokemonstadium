import time
from app.redis_client import check_redis
from app.db import check_db

def main():
  while True:
    # placeholder loop so the container staus alive
    check_db()
    check_redis()
    print("worker ok")
    time.sleep(10)

if __name__ == "__main__":
  main()