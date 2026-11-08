from pathlib import Path
import yt_dlp
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

url="https://www.youtube.com/watch?v=UkI9tKvvc4c"


def get_video_info(url):
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "js_runtimes": {
            "deno": {
                "path": r"C:\Users\yann1\.deno\bin\deno.exe"
            }
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title"),
                "duration": info.get("duration"),
                "thumbnail": info.get("thumbnail"),
                "format": info.get("format", []),
                "formats": [
                    {
                        "format_id": fmt.get("format_id"),
                        "ext": fmt.get("ext"),
                        "resolution": fmt.get("resolution"),
                        "fps": fmt.get("fps"),
                        "acodec": fmt.get("acodec"),
                        "vcodec": fmt.get("vcodec")
                    }
                    for fmt in info.get("formats", [])
                ]
            }

    except yt_dlp.utils.DownloadError as e:
        print("Erreur lors de l'extraction des informations :", str(e))
        return None
def get_available_qualities(formats):
    qualities = set()

    for fmt in formats:
        resolution = fmt.get("resolution")
        vcodec = fmt.get("vcodec")

        # On ignore les formats sans vidéo
        if not resolution or vcodec == "none":
            continue

        # Exemple : "1920x1080" devient ["1920", "1080"]
        if "x" in resolution:
            height = int(resolution.split("x")[1])
        else:
            continue

        if height in [360, 480, 720, 1080]:
            qualities.add(height)

    return sorted(qualities)


def download_video(url):
    ydl_opts = {
        "format": "18/best[acodec!=none][vcodec!=none]",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "noplaylist": True,
        "js_runtimes": {
            "deno": {
                "path": r"C:\Users\yann1\.deno\bin\deno.exe"
            }
        },
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        file_path = ydl.prepare_filename(info)

        if not Path(file_path).exists():
            raise FileNotFoundError("Vidéo téléchargée introuvable.")

        return file_path
def download_audio(url):
    ydl_opts = {
        "format": "140/bestaudio[ext=m4a]/bestaudio",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "noplaylist": True,
        "js_runtimes": {
            "deno": {
                "path": r"C:\Users\yann1\.deno\bin\deno.exe"
            }
        },
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        file_path = ydl.prepare_filename(info)

        if not Path(file_path).exists():
            raise FileNotFoundError("Fichier audio introuvable.")

        return file_path