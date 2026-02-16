import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from app.core.agent import run_agent

TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN not set")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_id = str(update.effective_user.id)
    text = update.message.text

    await update.message.chat.send_action("typing")

    reply = await run_agent(user_id, text)

    for i in range(0, len(reply), 4000):
        await update.message.reply_text(reply[i:i + 4000])


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("🚀 Production Telegram Bot Running...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
