from celery import shared_task
import time
from backend.interface.celery_config import celery_app
from backend.interface.redis_connection import get_redis_client


@shared_task
def test(x,y):
    redis_client = get_redis_client()
    lock = redis_client.lock("test_lock", timeout=10)

    if lock.acquire(blocking=False):
        try:
            print("locked, doing task")

            time.sleep(5)
            return x / y
        finally:
            lock.release()
            print("lock released")

    else:
        print("locked, skipping")
