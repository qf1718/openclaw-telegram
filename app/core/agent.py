from .session import SessionManager
from .gemini import ask_gemini

session_manager = SessionManager()


async def run_agent(user_id: str, message: str) -> str:
    history = session_manager.get_history(user_id)

    history.append({"role": "user", "content": message})

    response = await ask_gemini(history)

    history.append({"role": "assistant", "content": response})

    session_manager.save_history(user_id, history)

    return response
