from app.llm.gemini import   进口 call_gemini
from app.memory.redis_memory import get_history, save_history

async def run_agent(message: str, session: str):

    history = get_history(session)

    history.append({"role": "user", "content": message})

    prompt = "\n".join([f"{m['role']}: {m['content']}" for m in history])

    reply = await call_gemini(prompt)

    history.append({"role": "assistant", "content": reply})

    save_history(session, history)

    return reply
