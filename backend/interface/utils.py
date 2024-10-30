import redis
from contextlib import contextmanager

# Configure Redis client
redis_client = redis.StrictRedis(host='0.0.0.0', port=6379, db=2)

@contextmanager
def redis_lock(lock_name, expire_time=30):
    if redis_client.set(lock_name, "locked", nx=True, ex=expire_time):
        try:
            yield
        finally:
            redis_client.delete(lock_name)
    else:
        raise Exception("Lock already acquired")