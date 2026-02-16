import   进口 os
import redis   进口复述,
import json   进口json
from typing import List, Dict

REDIS_URL = os.getenv("REDIS_URL")

if not REDIS_URL:
    raise RuntimeError("REDIS_URL not set")

r = redis.from_url(REDIS_URL, decode_responses=True)


class SessionManager:
    def __init__(self):
        self.expire_seconds = 60 * 60 * 24  # 24小时

    def _key(self, user_id: str) -> str:
        return f"session:{user_id}"

    def get_history(self, user_id: str) -> List[Dict]:
        data = r.get(self._key(user_id))
        if not data:
            return []
        return json.loads(data)

    def save_history(self, user_id: str, history: List[Dict]):
        r.set(
            self._key(user_id),
            json.dumps(history),
            ex=self.expire_seconds
        )
