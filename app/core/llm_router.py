import os
import httpx
import asyncio

SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")
BASE_URL = os.getenv("SILICONFLOW_BASE_URL")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "glm-5")


class LLMRouter:

    @staticmethod
    async def chat(messages, model=None):
        model = model or DEFAULT_MODEL

        headers = {
            "Authorization": f"Bearer {SILICONFLOW_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.7
        }

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{BASE_URL}/chat/completions",
                headers=headers,
                json=payload
            )

        response.raise_for_status()
        data = response.json()

        return data["choices"][0]["message"]["content"]
