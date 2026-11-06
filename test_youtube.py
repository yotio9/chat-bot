import yt_dlp



ydl_opts={
    "quiet":True,
    "no_warning":True
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        print("Titre :", info.get("title"))
        print("Durée :", info.get("duration"), "secondes")
        print("Miniature :", info.get("thumbnail"))
        print("format :", info.get("format", []))
        formats = info.get("formats", [])
        for fmt in formats:
            print(
                "Format ID:", fmt.get("format_id"),
                "| Extension:", fmt.get("ext"),
                "| Résolution:", fmt.get("resolution"),
                "| FPS:", fmt.get("fps"),
                "| Audio:", fmt.get("acodec"),
                "| Vidéo:", fmt.get("vcodec")
            )

except yt_dlp.utils.DownloadError as e:
    print("Erreur lors de l'extraction des informations :", str(e))
