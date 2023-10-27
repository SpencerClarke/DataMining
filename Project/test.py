from pytube import YouTube
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

links_file = open("video_links.txt", "r")
i=0
for link in links_file:
    yt = YouTube(link)
    print(yt.title)

    yt.streams.filter(progressive = True,
    file_extension = "mp4").first().download(output_path = "./videos/",
    filename = str(i) + ".mp4")
    
    captions = yt.captions['a.en']
    captions_file = open("./videos/" + str(i) + "_captions.txt", "w")
    captions_file.write(captions.xml_captions)
    captions_file.close()

    i += 1

links_file.close()

for i in range(50):
    video = drive.CreateFile({'parents': [{'id': '157AZo06P3AnJrEdbO0gqYEO4oKnuagnO'}], "title": str(i) + ".mp4"})
    video.SetContentFile("./videos/" + str(i) + ".mp4")
    video.Upload()

    captions = drive.CreateFile({'parents': [{'id': '157AZo06P3AnJrEdbO0gqYEO4oKnuagnO'}], "title": str(i) + ".mp4"})
    captions.SetContentFile("./videos/" + str(i) + "_captions.txt")
    captions['title'] = str(i) + "_captions.txt"
    captions.Upload()