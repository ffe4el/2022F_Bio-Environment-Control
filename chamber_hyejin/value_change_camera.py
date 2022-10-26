import json
import serial.tools.list_ports
import serial
import time
import threading
import requests
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib
from flask import Flask, Response, jsonify

from flask_cors import cross_origin
# from value_print_2 import play
import pandas as pd
import winsound as ws
import schedule
import keyboard
import cv2
import numpy as np
from urllib.request import urlopen
import tensorflow as tf

app = Flask(__name__)



msg_level = "Ready..."
msg_growth = "Ready"


def camera_local():
    global msg_level
    url = "http://192.168.0.72:81/stream"  # ESP CAM의 영상 스트리밍 주소
    stream = urlopen(url)
    buffer = b''


    # Define the input size of the model
    input_size = (224, 224)

    # Load the saved model
    model = tf.keras.models.load_model("./keras_model.h5", compile=False)


    while True:
        if len(buffer) < 40960:
            buffer += stream.read(40960)
        head = buffer.find(b'\xff\xd8')
        end = buffer.find(b'\xff\xd9')
        # print(head, end, len(buffer))
        try:  # 가끔 비어있는 버퍼를 받아 오류가 발생함. 이를 위한 try문
            if head > -1 and end > -1:
                jpg = buffer[head:end + 2]
                buffer = buffer[end + 2:]
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

                # Resize the frame for the model
                model_frame = cv2.resize(frame, input_size, frame)

                # Expand Dimension (224, 224, 3) -> (1, 224, 224, 3) and Nomarlize the data
                model_frame = np.expand_dims(model_frame, axis=0) / 255.0

                # Predict
                is_level_prob = model.predict(model_frame)[0]
                is_level = np.argmax(is_level_prob)

                # Add Information on screen
                if is_level == 0:
                    msg_level = "NO"
                elif is_level == 1:
                    msg_level = "seed"
                elif is_level == 2:
                    msg_level = "sprout"
                elif is_level == 3:
                    msg_level = "growth"
                elif is_level == 4:
                    msg_level = "flower"
                elif is_level == 5:
                    msg_level = "fruit"
                # else:
                #     msg_level = "No"

                # msg_card += " ({:.1f})%".format(is_card_prob[is_card] * 100)

                # cv2.putText(frame, msg_level, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (225, 0, 0), thickness=2)


                ret, jpeg = cv2.imencode('.jpg', cv2.resize(frame, input_size, frame))
                jpeg = jpeg.tobytes()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg + b'\r\n\r\n')

        except:
            print("Hi")

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break



@app.route('/camera')
@cross_origin(origin='*')
def camera():
    return Response(camera_local(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/current_msg")
@cross_origin(origin='*')
def current_msg():
    global msg_level
    # camera_local()
    return msg_level




#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------


app.run(host="0.0.0.0", threaded=True, port=5001)



