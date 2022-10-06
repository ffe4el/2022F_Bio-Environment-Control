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
from flask import Flask, render_template, Response
from flask import Flask, render_template, Response
from cam_python import camera

app = Flask(__name__)
#10번 포트에 연결된 serial을 s로 지정(채널:9600)
s = serial.Serial('COM3', 9600)


@app.route('/')
def index():
    return 'Index Page'



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

@app.route('/video_feed')
def video_feed():
    return Response(camera(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


app.run(host="0.0.0.0")
