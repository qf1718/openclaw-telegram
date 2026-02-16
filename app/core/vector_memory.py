import redis
import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer

REDIS_URL = os.getenv("REDIS_URL")

r = redis.from_url(REDIS_URL)
model = SentenceTransformer("all-MiniLM-L6-v2")


class VectorMemory:

    @staticmethod
    def embed(text):
        return model.encode(text).tolist()

    @staticmethod
    def store(user_id, text):
        vector = VectorMemory.embed(text)
        key = f"memory:{user_id}"
        r.rpush(key, json.dumps({"text": text, "vector": vector}))

    @staticmethod
    def search(user_id, query, top_k=3):
        key = f"memory:{user_id}"
        items = r.lrange(key, 0, -1)

        query_vec = np.array(VectorMemory.embed(query))

        scored = []

        for item in items:
            obj = json.loads(item)
            vec = np.array(obj["vector"])
            score = np.dot(query_vec, vec)
            scored.append((score, obj["text"]))

        scored.sort(reverse=True)

        return [x[1] for x in scored[:top_k]]
