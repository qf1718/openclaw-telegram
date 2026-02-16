import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN not set")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    text = update.message.text
    user_id = update.effective_user.id

    reply = f"你说的是: {text}\n用户ID: {user_id}"

    await update.message.reply_text(reply)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("🚀 Telegram Bot Running...")

    # ❗ 不要用 asyncio.run
    # ❗ 不要 await
    # ❗ 直接 run_polling
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
