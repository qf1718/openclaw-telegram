from   从 .session import   进口 SessionManager
from .gemini import ask_gemini

session_manager = SessionManager()


async def run_agent(user_id: str, user_input: str) -> str:
    history = session_manager.get_history(user_id)

    history.append({
        "role": "user",
        "parts": [user_input]
    })

    reply = await ask_gemini(history)

    history.append({
        "role": "model",
        "parts": [reply]
    })

    session_manager.save_history(user_id, history)

    return reply   返回应答
