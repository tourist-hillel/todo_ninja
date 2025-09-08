import redis
import json
from django.conf import settings


class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
    
    def set_data(self, key, value, expire=None):
        if isinstance(value, dict):
            value = json.dumps(value)
        self.client.set(key, value)
        if expire:
            self.client.expire(key, expire)

    def get_data(self, key):
        value = self.client.get(key)
        if value:
            # try:
            #     return json.loads(value)
            # except json.JSONDecodeError:
                # return value
            return value
        return None
