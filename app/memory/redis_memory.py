import os
import redis
import json

redis_client = redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)

def get_history(session_id: str):
    data = redis_client.get(session_id)
    if not data:
        return []
    return json.loads(data)

def save_history(session_id: str, history):
    redis_client.set(session_id, json.dumps(history))
