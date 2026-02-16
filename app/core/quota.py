import redis
import os

r = redis.from_url(os.getenv("REDIS_URL"))

DAILY_LIMIT = 100


class QuotaManager:

    @staticmethod
    def check(user_id):
        key = f"quota:{user_id}"
        count = r.incr(key)

        if count == 1:
            r.expire(key, 86400)

        return count <= DAILY_LIMIT
