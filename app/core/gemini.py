import os
import httpx

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set")


async def ask_gemini(history):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    headers = {
        "Content-Type": "application/json",
    }

    contents = []

    for item in history:
        contents.append({
            "role": item["role"],
            "parts": [{"text": item["content"]}]
        })

    payload = {
        "contents": contents
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{url}?key={GEMINI_API_KEY}",
            headers=headers,
            json=payload,
            timeout=60,
        )

    data = response.json()

    return data["candidates"][0]["content"]["parts"][0]["text"]
