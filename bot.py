import os
import asyncio
import inspect
import httpx
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters


OPENCLAW_URL = os.getenv("OPENCLAW_URL")
TOKEN = os.getenv("TELEGRAM_TOKEN")


async def call_openclaw(text: str, session: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(
                OPENCLAW_URL,
                json={
                    "message": text,
                    "session": session
                }
            )
            return r.text
    except Exception as e:
        return f"❌ OpenClaw 调用失败: {e}"


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_text = update.message.text.strip()
    user_id = update.effective_user.id
    session = f"tg:{user_id}"

    await update.message.chat.send_action(ChatAction.TYPING)

    reply = await call_openclaw(user_text, session)

    for i in range(0, len(reply), 3500):
        await update.message.reply_text(reply[i:i+3500])


async def main():
    if not TOKEN:
        print("❌ TELEGRAM_TOKEN not set")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

    print("🚀 Telegram Bot Running...")
    await app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
