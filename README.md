# DataMining
A repository for the data mining course (Spencer Clarke)
I'm gonna be cooking up some heat

## Assignments completed
- probability assignment, located in HW1/probability_assignment.ipynb
- Ensemble learning, located in HW2/predict-ship-type.ipynb
- Midterm regression assignment using SGD, located in MidtermP1/take-at-home.ipynb
- A wavenet assignment located in wavenet/wavenet.ipynb

## Project milestones completed
- Milestone 1, downloading a library of youtube videos and uploading to Google Drive, located in Project/
    - If this were not a graded assignment, I would also never have uploaded the large video files to this repository as it is poor practice to do so. I am uploading them so that you can see that the videos were successfully downloaded, but I just want you to know that I did not enjoy doing so.

    - In addition, there is also an image of the files successfully uploaded to Google Drive in Project/gdrive.png

- Milestone 2, video indexing. located in Project/video_indexing/
    - Firstly, I ripped frames from the videos as jpg files using a bash script calling ffmpeg, located in Project/video_indexing/get_frames.sh

	- Next, for the rest of the milestone, I put the code into a single ipynb for clarity of each step of the process. It is located at Project/video_indexing/video_indexing.ipynb . I used Pytorch to create the autoencoder, and I used postgresql with pgvector to store the embeddings of the frames, and have included an image search query where I give it an input image from the dataset, and using the <-> operator from pgvector, it gives me back the embeddings of the 10 most similar frames by taking the euclidan distances between the vectors containing the embedded images. I then took these embeddings and decoded them to reveal the similarity. This query and its results can be seen towards the bottom of the ipynb file.

- Milestone 3, text indexing

- Milestone 4, fusion of image and text embeddings

- Milestone 5, graphical interface 
    - I modified milestone 4 into a new notebook at Project/Milestone_4/video_retrieval.ipynb which I used to obtain the dual encoder, which is now trained on video frames and video captions, rather than the captioned images from the huggingface dataset, and also to put the dual-encodings of the videos into the database. I trained the dual-encoder in batches so there are keyboard interrupts among other ugly things in that notebook. The only data used to train the final model was the videos and their captions, which are available in this repository under Project/videos. The frontend was written in HTML and is served by an Apache web server, and it gets the predicted videos via a REST API written in python with Flask. These two components can be seen in Project/html, which contains everything needed to build the app (including the trained dual-encoder produced by video_retrieval.ipynb). Unless something went wrong, the app should be hosted here. I will leave this running 24/7 until this milestone is graded.
    [http://thinkcenter.ddns.me/](http://thinkcenter.ddns.me/)