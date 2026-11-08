import asyncio
from app.services.youtube import download_video, download_audio

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes
from telegram.request import HTTPXRequest
from telegram.ext import MessageHandler, filters
from app.services.youtube import get_video_info

from app.config import TELEGRAM_BOT_TOKEN


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Commande reçue !")

    await update.message.reply_text(
        "Bienvenue ! Je suis ton assistant de téléchargement YouTube. 🎬"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "youtube.com/" not in url and "youtu.be/" not in url:
        await update.message.reply_text(
            "Envoie-moi un lien YouTube valide."
        )
        return

    await update.message.reply_text(
        "⏳ Récupération des informations de la vidéo..."
    )

    try:
        info = await asyncio.to_thread(get_video_info, url)

        title = info.get("title") or "Titre inconnu"
        thumbnail = info.get("thumbnail")
        duration = info.get("duration")

        if duration is not None:
            hours, remainder = divmod(int(duration), 3600)
            minutes, seconds = divmod(remainder, 60)

            if hours:
                duration_text = f"{hours}:{minutes:02d}:{seconds:02d}"
            else:
                duration_text = f"{minutes}:{seconds:02d}"
        else:
            duration_text = "Inconnue"

        video_id = info.get("id")

        context.user_data[f"youtube_url_{video_id}"] = url

        keyboard = [
            [
                InlineKeyboardButton(
                    "🎬 Télécharger la vidéo",
                    callback_data=f"video:{video_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    "🎵 Télécharger en MP3",
                    callback_data=f"audio:{video_id}",
                )
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        caption = (
            f"🎬 {title}\n"
            f"⏱ Durée : {duration_text}\n\n"
            "Choisis le format de téléchargement :"
        )

        if thumbnail:
            try:
                await update.message.reply_photo(
                    photo=thumbnail,
                    caption=caption,
                    reply_markup=reply_markup,
                )
            except Exception:
                await update.message.reply_text(
                    caption,
                    reply_markup=reply_markup,
                )
        else:
            await update.message.reply_text(
                caption,
                reply_markup=reply_markup,
            )

    except Exception as error:
        print(f"Erreur lors de la récupération : {error}")

        await update.message.reply_text(
            "Impossible de récupérer les informations de cette vidéo. Réessaie avec un autre lien."
        )

async def handle_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    action, video_id = query.data.split(":", 1)

    url = context.user_data.get(f"youtube_url_{video_id}")

    if not url:
        await query.message.reply_text(
            "Ce lien n'est plus disponible. Envoie-le à nouveau."
        )
        return

    await query.message.reply_text(
        "⏳ Téléchargement en cours..."
    )

    try:
        if action == "video":
            file_path = await asyncio.to_thread(download_video, url)

            with open(file_path, "rb") as video_file:
                await query.message.reply_video(
                    video=video_file,
                    caption="Voici ta vidéo ! 🎬"
                )

        elif action == "audio":
            file_path = await asyncio.to_thread(download_audio, url)

            with open(file_path, "rb") as audio_file:
                await query.message.reply_audio(
                    audio=audio_file,
                    title="Audio YouTube",
                    caption="Voici ton audio ! 🎵"
                )

    except Exception as error:
        print(f"Erreur de téléchargement : {error}")

        await query.message.reply_text(
            "Le téléchargement a échoué. Vérifie le lien ou réessaie."
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

    application.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    application.add_handler(
    CallbackQueryHandler(
        handle_download,
        pattern=r"^(video|audio):"
    )
)

    print("Le bot Telegram est démarré !")

    application.run_polling()


if __name__ == "__main__":
    main()
