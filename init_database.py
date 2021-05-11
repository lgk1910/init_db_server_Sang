import pandas as pd
from tqdm import tqdm
from tqdm import trange

listing_url=pd.read_csv("unique_listing.csv")
listing_url=listing_url.set_index('Code')
listing_url=pd.DataFrame.transpose(listing_url)
listing_url=listing_url.fillna("MISSING")

from app import db
from app import Table

db.create_all()

import numpy as np
import pandas as pd
import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
from skimage import io
import os
import pickle
import requests

way_in_model =  tf.keras.Sequential([
    hub.KerasLayer("https://hub.tensorflow.google.cn/tensorflow/efficientnet/b0/feature-vector/1",
                   trainable=False)
])
way_in_model.build([None, 224, 224, 3]) 

pickle_in = open("K_means_model","rb")
km = pickle.load(pickle_in)

try:
    os.mkdir('dataset')
except:
    pass

def url_to_Kmean_class(url):
    img = io.imread(url)
    img=cv2.resize(img,(224,224))
    img=(img/255.0).astype('float16')
    return km.predict(way_in_model.predict(np.array([img])))[0]

list_listing=[]
for i in listing_url:
    list_listing.append(i)

for i in tqdm(range(0,len(list_listing))):
    try:
        os.mkdir(f'dataset/{list_listing[i]}')
    except:
        pass
    for id, img in enumerate(listing_url[list_listing[i]]):
        if (img=="MISSING"):
            break
        try:
            a=Table(img,list_listing[i],int(url_to_Kmean_class(img)))
            response = requests.get(img)
            with open(f'dataset/{list_listing[i]}/img{id}.jpg', 'wb') as f:
                f.write(response.content)
            db.session.add(a)
            db.session.commit()
        except:
            pass

print("MISSION COMPLETED")