#시리얼 통신 라이브러리
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
from flask import Flask, Response
# from cam_python import camera
from flask_cors import cross_origin


app = Flask(__name__)
#3번 포트에 연결된 serial을 s로 지정(채널:9600)(COM3)
s = serial.Serial('COM3', 9600)

msg_level = "Ready"

import cv2
import numpy as np
from urllib.request import urlopen
import tensorflow as tf

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
        print(head, end, len(buffer))
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
                    msg_level = "seed"
                elif is_level == 1:
                    msg_level = "sprout"
                elif is_level == 2:
                    msg_level = "growth"
                elif is_level == 3:
                    msg_level = "flower"
                elif is_level == 4:
                    msg_level = "fruit"
                else:
                    msg_level = "nothing"

                # msg_card += " ({:.1f})%".format(is_card_prob[is_card] * 100)

                cv2.putText(frame, msg_level, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (225, 0, 0), thickness=2)


                ret, jpeg = cv2.imencode('.jpg', cv2.resize(frame, input_size, frame))
                jpeg = jpeg.tobytes()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg + b'\r\n\r\n')

        except:
            print("Hi")

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break


@app.route('/')
@cross_origin(origin='*')
def index():
    return Response(camera_local(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/current_msg")
@cross_origin(origin='*')
def current_msg():
    return msg_level



def send_signal_to_sfarm(msg):
    while True:
        z = s.readline()
        # print(z)
        # 내용이 비어있지 않으면 프린트

        if not z.decode().startswith("#"):
            z = z.decode()[:len(z) - 1]
            print("내용출력:", end="")
            print(z)
            if z.startswith("{ \"temp"):
                data = json.loads(z)
                temp = int(data["temp"])
        else:
            break
    if (s.readable()):
        s.write("{}\n".format(msg).encode())

def load_env():
    z = s.readline()
    z = z.decode()[:len(z) - 1]
    data = json.loads(z)
    temp = int(data["temp"])
    humid = int(data['humidity'])
    cdc = int(data['cdc'])
    print(temp, humid, cdc)
    return temp, humid, cdc

# def random_sinegraph():
#     matplotlib.use('TkAgg')
#     plt.rcParams["figure.figsize"] = [7.50, 3.50]
#     plt.rcParams["figure.autolayout"] = True
#
#     temp_threshold = 28
#
#     fig = plt.figure()
#     ax = plt.axes(xlim=(0, 2), ylim=(18, 32))
#     ax.set_ylabel("Indoor temperature (degrees C)")
#     ax.set_xlabel("time line")
#     line, = ax.plot([], [], lw=2)
#
#     plt.axhline(y=temp_threshold, ls="--")
#     line_color = "b"
#     stage = -1

@app.route('/fan-on')
def fan_on():
    send_signal_to_sfarm("C_F-1")
    load_env()
    return "Order Fan On"



@app.route('/fan-off')
def fan_off():
    send_signal_to_sfarm("C_F-0")
    return "Order Fan Off"

@app.route('/light-on/<level>')
def light_on(level):
    send_signal_to_sfarm("C_L-{}".format(level))
    return f"Order Light {level}"

# @app.route('/light-on')
# def light_on():
#     send_signal_to_sfarm("C_L-10")
#     return "Order Light 10"

@app.route('/light-off')
def light_off():
    send_signal_to_sfarm("C_L-0")
    return "Order Light 0"

@app.route('/window-open')
def window_open():
    send_signal_to_sfarm("C_S-1")
    return "Order window open"

@app.route('/window-close')
def window_close():
    send_signal_to_sfarm("C_S-0")
    return "Order window close"


app.run(host="0.0.0.0", threaded=True)
