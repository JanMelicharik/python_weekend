import redis

redis_config = {
    "host": "redis.pythonweekend.skypicker.com",
    "port": 6379,
    "socket_connect_timeout": 3,
    "decode_responses": True,
}


def init_redis():
    return redis.Redis(**redis_config)
