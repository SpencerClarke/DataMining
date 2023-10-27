from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

for i in range(50):
    video = drive.CreateFile({'parents': [{'id': '157AZo06P3AnJrEdbO0gqYEO4oKnuagnO'}], "title": str(i) + ".mp4"})
    video.SetContentFile("./videos/" + str(i) + ".mp4")
    video.Upload()

    captions = drive.CreateFile({'parents': [{'id': '157AZo06P3AnJrEdbO0gqYEO4oKnuagnO'}], "title": str(i) + ".mp4"})
    captions.SetContentFile("./videos/" + str(i) + "_captions.txt")
    captions['title'] = str(i) + "_captions.txt"
    captions.Upload()