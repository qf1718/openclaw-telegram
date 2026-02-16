class ToolEngine:

    @staticmethod
    async def maybe_use_tool(text):
        if "天气" in text:
            return "今天晴天 25°C"
        if "时间" in text:
            import datetime
            return str(datetime.datetime.now())
        return None
