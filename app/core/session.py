import os
import json
import redis


class SessionManager:
    def __init__(self):
        redis_url = os.getenv("REDIS_URL")

        if not redis_url:
            raise RuntimeError("REDIS_URL not set")

        self.client = redis.from_url(redis_url, decode_responses=True)

    def get_history(self, user_id: str):
        data = self.client.get(user_id)
        if data:
            return json.loads(data)
        return []

    def save_history(self, user_id: str, history):
        self.client.set(user_id, json.dumps(history), ex=86400)
