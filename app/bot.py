from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.request import HTTPXRequest
from telegram.ext import MessageHandler, filters

from app.config import TELEGRAM_BOT_TOKEN


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Commande reçue !")

    await update.message.reply_text(
        "Bienvenue ! Je suis ton assistant de téléchargement YouTube. 🎬"
    )


def main():
    request = HTTPXRequest(
        connect_timeout=30,
        read_timeout=30,
        write_timeout=30,
        pool_timeout=30
    )

    application = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .request(request)
        .build()
    )

    application.add_handler(CommandHandler("start", start))

    print("Le bot Telegram est démarré !")

    application.run_polling()


if __name__ == "__main__":
    main()