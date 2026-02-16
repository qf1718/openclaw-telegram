from .llm_router import LLMRouter
from .vector_memory import VectorMemory
from .quota import QuotaManager
from .tool_engine import ToolEngine


async def run_agent(user_id, text):

    if not QuotaManager.check(user_id):
        return "今日额度已用完"

    tool_result = await ToolEngine.maybe_use_tool(text)
    if tool_result:
        return tool_result

    memories = VectorMemory.search(user_id, text)

    messages = []

    if memories:
        messages.append({
            "role": "system",
            "content": "以下是相关记忆：" + "\n".join(memories)
        })

    messages.append({
        "role": "user",
        "content": text
    })

    reply = await LLMRouter.chat(messages)

    VectorMemory.store(user_id, text)

    return reply
