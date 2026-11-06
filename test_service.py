from app.services.youtube import get_video_info, get_available_qualities, download_video, download_audio

url ="https://www.youtube.com/watch?v=IvQJVKrl0pQ&list=RDIvQJVKrl0pQ&start_radio=1"


print("\nTéléchargement audio en cours...")

audio_path = download_audio(url)

print("\nTéléchargement audio terminé !")
print("Fichier :", audio_path)



############################################################
#video = get_video_info(url)


#video = get_video_info(url)

#print("Titre :", video["title"])

#print("\nTéléchargement en cours...")

#file_path = download_video(url)

#print("\nTéléchargement terminé !")
#print("Fichier :", file_path)
###########################################################@
#print("Titre :", video["title"])
#print("Durée :", video["duration"], "secondes")

#print("Miniature :", video["thumbnail"])

#qualities = get_available_qualities(video["formats"])

#print("\nQualités disponibles :")
#print(qualities)