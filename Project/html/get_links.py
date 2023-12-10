from flask import Flask
from flask_cors import CORS
from flask import request

import torch
import torch
import random
import torchvision
import os
import numpy
import psycopg2
import os
import gensim.downloader

def encode_caption_string(caption_string):
    encodings = []
    for caption in caption_string:
        if caption in glove_vectors:
            encodings.append(glove_vectors[caption])
    if len(encodings) == 0:
        return None
    return numpy.mean(encodings, axis=0)

print("Loading glove vectors")
glove_vectors = gensim.downloader.load('glove-twitter-200')

print("Loading dual encoder")
class CNN2(torch.nn.Module):
    def __init__(self):
        super(CNN2, self).__init__()
        #These will project the image and text encodings to be 1875-dimensional vectors
        #So that we can take the dot product between image and text encodings
        self.project_image = torch.nn.Sequential(
            torch.nn.Flatten(1, -1),
            torch.nn.Linear(1875, 1875),
            torch.nn.ReLU(),
            torch.nn.Linear(1875, 1875),
            torch.nn.ReLU(),
            torch.nn.Linear(1875, 1875)
        )
        self.project_text = torch.nn.Sequential(
            torch.nn.Linear(200, 1875),
            torch.nn.ReLU(),
            torch.nn.Linear(1875, 1875),
            torch.nn.ReLU(),
            torch.nn.Linear(1875, 1875)
        )
         
    #We will train the network to predict its own input by compressing and then decompressing it
    def forward(self, word_encodings, image_encodings):
        word_encodings = self.project_text(word_encodings)
        word_encodings = torch.nn.functional.normalize(word_encodings)
        image_encodings = self.project_image(image_encodings)
        image_encodings = torch.nn.functional.normalize(image_encodings)
        #The dot similarity is the dot product of a word encodnig and an image encoding
        #This works because the dot product acts a measure for similarity
        #And this matrix multiplication will get the dot product of every row in A with every row in B
        return word_encodings, image_encodings
    
cnn2 = CNN2()
cnn2.load_state_dict(torch.load("./cnn2.pth", map_location=torch.device("cpu")))


app = Flask(__name__)
CORS(app)

@app.route("/get_links")
def summary():

    if("query" in request.headers):   
        if(isinstance(request.headers["query"], str)):
            conn = psycopg2.connect(
            host="localhost",
            database="datamining",
            user="msbean",
            password="cactusgreen")

            conn.autocommit = True
            cursor = conn.cursor() 

            encoded_string = encode_caption_string(request.headers["query"].lower().split(" "))
            if encoded_string is None:
                return []
            encoding = torch.stack([torch.FloatTensor(encoded_string)])
            encoding = cnn2.project_text(encoding)

            sql = "SELECT youtube_link FROM projected_video_embeddings ORDER BY embedding <-> '["
            flattened = encoding.flatten().tolist()
            for datum in flattened:
                sql += str(datum) + ","
            sql = sql[:-1]
            sql += "]' LIMIT 3"

            cursor.execute(sql)
            result = cursor.fetchall()

            conn.commit() 
            conn.close()

            response_links = [[r[0] for r in result]]
            return response_links
        else:
            return ["Invalid query"]
    return ["No headers"]


def create_app():
    return app
