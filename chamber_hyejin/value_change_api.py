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
from flask import Flask, Response, jsonify, request

from flask_cors import cross_origin
# from value_print_2 import play
import pandas as pd
import winsound as ws
import schedule
import keyboard
import cv2
import numpy as np
import tensorflow as tf

app = Flask(__name__)

msg_growth_str = None
# 3번 포트에 연결된 serial을 s로 지정(채널:9600)(COM3)
# 아두이노 메가
s = serial.Serial('COM3', 9600)
# # 아두이노 우노
ss = serial.Serial('COM6', 9600)  # 아두이노 우노


# 아두이노 메가에 신호보내기
@app.route('/send_signal_sfarm', methods=["post"])
@cross_origin(origin='*')
def send_signal_to_sfarm_post():
    msg = request.json["msg"]
    print("set send_signal_sfarm", msg)
    send_signal_to_sfarm(msg)
    return '', 200


def send_signal_to_sfarm(msg):
    if (s.readable()):
        s.write("{}\n".format(msg).encode())
    else:
        print("message is not transferred")


# 아두이노 우노에 신호보내기
@app.route('/send_signal_ssfarm', methods=["post"])
@cross_origin(origin='*')
def send_signal_to_ssfarm_post():
    msg = request.json["msg"]
    print("set send_signal_ssfarm", msg)
    send_signal_to_ssfarm(msg)
    return '', 200


def send_signal_to_ssfarm(msg):
    if (ss.readable()):
        ss.write("{}\n".format(msg).encode())
    else:
        print("message is not transferred")


@app.route("/set_scenario", methods=["post"])
@cross_origin(origin='*')
def set_message():
    msg = request.json["msg"]
    global msg_growth_str
    print("set scenario", msg)
    msg_growth_str = msg
    return '', 200

# 환경값 받아오기
def load_env_msg():
    data = ""
    while True:
        z = s.readline()

        if not z.decode().startswith("#"):
            z = z.decode()[:len(z) - 1]
        # if not z.startswith(b"#"):
        #     z = z[:len(z) - 1]
            if z.startswith("{ \"temp"):
                data = json.loads(z)
                # temp = int(data["temp"])
                print("내용출력:", end="")
                print(z)
                return z
            else:
                print("this message is ignored.")
                print(z)
        else:
            print("start with #")
            print(z)
    return data


@app.route("/env_msg")
@cross_origin(origin='*')
def env_msg():
    return Response(load_env_msg(), mimetype='application/json')


@app.route('/fan-on')
def fan_on():
    send_signal_to_sfarm("C_F-1")
    print("fan on")
    return "Order Fan On"
@app.route('/fan-off')
def fan_off():
    send_signal_to_sfarm("C_F-0")
    print("fan off")
    return "Order Fan Off"

# led 조명
@app.route('/light-on/<level>')
def light_on(level):
    send_signal_to_sfarm("C_L-{}".format(level))
    return f"Order Light {level}"
@app.route('/light-off')
def light_off():
    send_signal_to_sfarm("C_L-0")
    return "Order Light 0"

# 창문
@app.route('/window-open')
def window_open():
    send_signal_to_sfarm("C_S-1")
    return "Order window open"
@app.route('/window-close')
def window_close():
    send_signal_to_sfarm("C_S-0")
    return "Order window close"

# 발열등
@app.route('/red-on')
def red_on():
    send_signal_to_ssfarm("R1")
    return "Order red on"
@app.route('/red-off')
def red_off():
    send_signal_to_ssfarm("R0")
    return "Order red off"

# 안개분무기
@app.route('/blue-on')
def blue_on():
    send_signal_to_ssfarm("B1")
    return "Order blue on"
@app.route('/blue-off')
def blue_off():
    send_signal_to_ssfarm("B0")
    return "Order blue off"

# 수분공급기
@app.route('/white-on')
def white_on():
    send_signal_to_ssfarm("W1")
    return "Order red on"
@app.route('/white-off')
def white_off():
    send_signal_to_ssfarm("W0")
    return "Order white off"

# Co2 발생기
@app.route('/yellow-on')
def yellow_on():
    send_signal_to_ssfarm("Y1")
    return "Order yellow on"
@app.route('/yellow-off')
def yellow_off():
    send_signal_to_ssfarm("Y0")
    return "Order yellow off"

# O2 발생기
@app.route('/green-on')
def green_on():
    send_signal_to_ssfarm("G1")
    return "Order green on"
@app.route('/green-off')
def green_off():
    send_signal_to_ssfarm("G0")
    return "Order green off"

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def beepsound():
    freq = 2000    # range : 37 ~ 32767
    dur = 150    # ms
    ws.Beep(freq, dur) # winsound.Beep(frequency, duration)


df = pd.read_csv("data/control_rules.csv")
df["season_level"] = df["season"] + " " + df["level"]
print(df.head())


@app.route("/msg_growth")
@cross_origin(origin='*')
def msg_growth():
    # URL = 'http://localhost:5001/current_msg'
    # response = requests.get(URL)
    # print(response.text)
    # msg_growth_str = response.text
    global msg_growth_str

    if msg_growth_str is None:
        resp = {
            "name": "Interactive mode",
            "toggle-demo": "off",
            "win_btn": "off",
            "light_btn": "off",
            "fog_btn": "off",
            "co2_btn": "off",
            "heater_btn": "off",
            "o2_btn": "off",
            "water_btn": "off",
        }
    else:
        record = df[df["season_level"] == msg_growth_str]

        resp = {
            "name": msg_growth_str,
            "toggle-demo": record["fan"].item(),
            "win_btn": record["window"].item(),
            "light_btn": record["light"].item(),
            "fog_btn": record["fog"].item(),
            "co2_btn": record["co2"].item(),
            "heater_btn": record["heat"].item(),
            "o2_btn": record["o2"].item(),
            "water_btn": record["water"].item(),
        }

    print(resp)

    return jsonify(resp), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True, port=5000)
