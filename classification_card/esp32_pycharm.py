import tensorflow as tf
import cv2
import numpy as np
from urllib.request import urlopen
import requests
from http.client import IncompleteRead

# Define the input size of the model
input_size = (224, 224)

# Open streaming url
# change to ESP32-CAM ip

url = "http://192.168.0.72/"
# url = "http://192.168.219.112:81/stream"
CAMERA_BUFFER_SIZE = 4096
stream = urlopen(url)
bts = b''

# Load the saved model
model = tf.keras.models.load.model("keras_model.h5", complie=False)

oldURL = ''
while True:
    try:
        bts += stream.read(CAMERA_BUFFER_SIZE)
    except IncompleteRead:
        print("streaming error has occurred")

    jpghead = bts.find(b'\xff\xd8')
    jpgend = bts.find(b'\xff\xd9')

    if jpghead > -1 and jpgend > -1:
        jpg = bts[jpghead:jpgend + 2]
        bts = bts[jpgend +2:]
        img = cv2.imdecode(np.frombuffer(jpg, dtype = np.unit8), cv2.IMREAD_UNCANGED)
        v = cv2.flip(img, 0)
        h = cv2.flip(img, 1)
        p = cv2.flip(img, -1)
        frame = pdbh, w = frame.shape[:2]
        img = cv2.resize(frame, (888, 688))


