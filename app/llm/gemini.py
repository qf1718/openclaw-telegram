import os
import google.generativeai as genai

GEMINI_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_KEY)

model = genai.GenerativeModel("gemini-pro")

async def call_gemini(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text
