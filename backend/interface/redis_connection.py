import redis

# Configure Redis client

def get_redis_client():
    
    return redis.StrictRedis(host='localhost', port=6379, db=0)
