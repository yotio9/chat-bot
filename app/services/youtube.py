from pathlib import Path
import yt_dlp

url="https://www.youtube.com/watch?v=UkI9tKvvc4c"


def get_video_info(url):
    

    ydl_opts = {
        "quiet": True,
        "no_warning": True,
        "noplaylist": True
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
        "format": "bestvideo+bestaudio/best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "merge_output_format": "mp4",
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


def download_audio(url):
    ydl_opts={
        "format":"bestaudio/best",
        "outtmpl":" downloads/%(title)s.%(ext)s",
        "noplaylist":True,
        "postprocessors":[
            {
                "key":"FFmpegExtractAudio",
                "preferredcodec":"mp3",
                "preferredquality":"192",

            }
        ]

    }  

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info= ydl.extract_info(url,download=True)
        original_path=Path(ydl.prepare_filemane(info))
        mp3_path =original_path.with_suffix(".mp3")

        if mp3_path.exists():
            return str(mp3_path)

        raise FileNotFoundError(" le fichier MP3 na pas ete créér.")