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
#3번 포트에 연결된 serial을 s로 지정(채널:9600)(COM3)
# 아두이노 메가
s = serial.Serial('COM3', 9600)
# # 아두이노 우노
ss = serial.Serial('COM6', 9600)  # 아두이노 우노


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

# 아두이노 메가에 신호보내기
def send_signal_to_sfarm(msg):
    if (s.readable()):
        s.write("{}\n".format(msg).encode())
    else:
        print("message is not transferred")

# 아두이노 우노에 신호보내기
def send_signal_to_ssfarm(msg):
    if (ss.readable()):
        ss.write("{}\n".format(msg).encode())
    else:
        print("message is not transferred")

# 환경값 받아오기
def load_env_msg():
    data = ""
    while True:
        z = s.readline()

        if not z.decode().startswith("#"):
            z = z.decode()[:len(z) - 1]
        # if not z.startswith(b"#"):
        #     z = z[:len(z) - 1]
            if z.startswith(""):
                data = json.loads(z)
                # temp = int(data["temp"])
                print("내용출력:", end="")
                print(z)
                return z
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

# 여름 1단계
def summer_first():
    # fan
    send_signal_to_sfarm("C_F-0")
    # heat
    send_signal_to_ssfarm("RO")
    # light
    send_signal_to_sfarm("C_L-9")
    # fog
    send_signal_to_ssfarm("B0")
    # window
    send_signal_to_sfarm("C_S-1")
    # co2
    send_signal_to_ssfarm("Y1")
    # o2
    send_signal_to_ssfarm("G0")
    # water
    send_signal_to_ssfarm("W1")
    # sound
    beepsound()

# 여름 2단계
def summer_second():
    # fan
    send_signal_to_sfarm("C_F-1")
    # heat
    send_signal_to_ssfarm("RO")
    # light
    send_signal_to_sfarm("C_L-6")
    # fog
    send_signal_to_ssfarm("B0")
    # window
    send_signal_to_sfarm("S1")
    # co2
    send_signal_to_ssfarm("Y1")
    # o2
    send_signal_to_ssfarm("G0")
    # water
    send_signal_to_ssfarm("W1")
    # sound
    beepsound()

# 여름 3-1단계
def summer_third1():
    # fan
    send_signal_to_ssfarm("C_F-1")
    # heat
    send_signal_to_sfarm("RO")
    # light
    send_signal_to_sfarm("C_L-7")
    # fog
    send_signal_to_ssfarm("B0")
    # window
    send_signal_to_sfarm("C_S-1")
    # co2
    send_signal_to_ssfarm("Y1")
    # o2
    send_signal_to_ssfarm("G0")
    # water
    send_signal_to_ssfarm("W1")
    # sound
    beepsound()

# 여름 3-2단계
def summer_third2():
    # fan
    send_signal_to_sfarm("C_F-1")
    # heat
    send_signal_to_ssfarm("RO")
    # light
    send_signal_to_sfarm("C_L-0")
    # fog
    send_signal_to_ssfarm("B0")
    # window
    send_signal_to_sfarm("C_S-1")
    # co2
    send_signal_to_ssfarm("Y0")
    # o2
    send_signal_to_ssfarm("G1")
    # water
    send_signal_to_ssfarm("W0")
    # sound
    beepsound()

# 여름 4단계
def summer_forth():
    # fan
    send_signal_to_sfarm("C_F-1")
    # heat
    send_signal_to_ssfarm("RO")
    # light
    send_signal_to_sfarm("C_L-5")
    # fog
    send_signal_to_ssfarm("B0")
    # window
    send_signal_to_sfarm("C_S-1")
    # co2
    send_signal_to_ssfarm("Y1")
    # o2
    send_signal_to_ssfarm("G1")
    # water
    send_signal_to_ssfarm("W1")
    # sound
    beepsound()

# 여름 5단계
def summer_fifth():
    # fan
    send_signal_to_sfarm("C_F-1")
    # heat
    send_signal_to_ssfarm("RO")
    # light
    send_signal_to_sfarm("C_L-8")
    # fog
    send_signal_to_ssfarm("B0")
    # window
    send_signal_to_sfarm("C_S-1")
    # co2
    send_signal_to_ssfarm("Y1")
    # o2
    send_signal_to_ssfarm("G1")
    # water
    send_signal_to_ssfarm("W1")
    # sound
    beepsound()

# 겨울 1단계
def winter_first():
    # fan
    send_signal_to_sfarm("C_F-1")
    # heat
    send_signal_to_ssfarm("R1")
    # light
    send_signal_to_sfarm("C_L-9")
    # fog
    send_signal_to_ssfarm("B1")
    # window
    send_signal_to_sfarm("C_S-0")
    # co2
    send_signal_to_ssfarm("Y1")
    # o2
    send_signal_to_ssfarm("G0")
    # water
    send_signal_to_ssfarm("W1")
    # sound
    beepsound()

# 겨울 2단계
def winter_second():
    # fan
    send_signal_to_sfarm("C_F-0")
    # heat
    send_signal_to_ssfarm("R1")
    # light
    send_signal_to_sfarm("C_L-9")
    # fog
    send_signal_to_ssfarm("B1")
    # window
    send_signal_to_sfarm("C_S-0")
    # co2
    send_signal_to_ssfarm("Y1")
    # o2
    send_signal_to_ssfarm("G0")
    # water
    send_signal_to_ssfarm("W1")
    # sound
    beepsound()

# 겨울 3-1단계
def winter_third1():
    # fan
    send_signal_to_sfarm("C_F-0")
    # heat
    send_signal_to_ssfarm("R1")
    # light
    send_signal_to_sfarm("C_L-7")
    # fog
    send_signal_to_ssfarm("B1")
    # window
    send_signal_to_sfarm("C_S-1")
    # co2
    send_signal_to_ssfarm("Y1")
    # o2
    send_signal_to_ssfarm("G0")
    # water
    send_signal_to_ssfarm("W0")
    # sound
    beepsound()

# 겨울 3-2단계
def winter_third2():
    # fan
    send_signal_to_sfarm("C_F-0")
    # heat
    send_signal_to_ssfarm("R1")
    # light
    send_signal_to_sfarm("C_L-0")
    # fog
    send_signal_to_ssfarm("B1")
    # window
    send_signal_to_sfarm("C_S-0")
    # co2
    send_signal_to_ssfarm("Y0")
    # o2
    send_signal_to_ssfarm("G1")
    # water
    send_signal_to_ssfarm("W0")
    # sound
    beepsound()

# 겨울 4단계
def winter_forth():
    # fan
    send_signal_to_sfarm("C_F-0")
    # heat
    send_signal_to_ssfarm("R1")
    # light
    send_signal_to_sfarm("C_L-6")
    # fog
    send_signal_to_ssfarm("B1")
    # window
    send_signal_to_sfarm("C_S-0")
    # co2
    send_signal_to_ssfarm("Y1")
    # o2
    send_signal_to_ssfarm("G0")
    # water
    send_signal_to_ssfarm("W0")
    # sound
    beepsound()

# 겨울 5단계
def winter_fifth():
    # fan
    send_signal_to_sfarm("C_F-0")
    # heat
    send_signal_to_ssfarm("R1")
    # light
    send_signal_to_sfarm("C_L-8")
    # fog
    send_signal_to_ssfarm("B1")
    # window
    send_signal_to_sfarm("C_S-0")
    # co2
    send_signal_to_ssfarm("Y1")
    # o2
    send_signal_to_ssfarm("G0")
    # water
    send_signal_to_ssfarm("W0")
    # sound
    beepsound()

# 비 1단계
def rain_first():
    # fan
    send_signal_to_sfarm("C_F-1")
    # heat
    send_signal_to_ssfarm("R1")
    # light
    send_signal_to_sfarm("C_L-9")
    # fog
    send_signal_to_ssfarm("B0")
    # window
    send_signal_to_sfarm("C_S-0")
    # co2
    send_signal_to_ssfarm("Y1")
    # o2
    send_signal_to_ssfarm("G0")
    # water
    send_signal_to_ssfarm("W1")
    # sound
    beepsound()

# 비 2단계
def rain_second():
    # fan
    send_signal_to_sfarm("C_F-1")
    # heat
    send_signal_to_ssfarm("RO")
    # light
    send_signal_to_sfarm("C_L-7")
    # fog
    send_signal_to_ssfarm("B0")
    # window
    send_signal_to_sfarm("C_S-0")
    # co2
    send_signal_to_ssfarm("Y1")
    # o2
    send_signal_to_ssfarm("G0")
    # water
    send_signal_to_ssfarm("W1")
    # sound
    beepsound()

# 비 3-1단계
def rain_third1():
    # fan
    send_signal_to_sfarm("C_F-1")
    # heat
    send_signal_to_ssfarm("R1")
    # light
    send_signal_to_sfarm("C_L-6")
    # fog
    send_signal_to_ssfarm("B0")
    # window
    send_signal_to_sfarm("C_S-0")
    # co2
    send_signal_to_ssfarm("Y1")
    # o2
    send_signal_to_ssfarm("G0")
    # water
    send_signal_to_ssfarm("W0")
    # sound
    beepsound()

# 비 3-2단계
def rain_third2():
    # fan
    send_signal_to_sfarm("C_F-1")
    # heat
    send_signal_to_ssfarm("RO")
    # light
    send_signal_to_sfarm("C_L-0")
    # fog
    send_signal_to_ssfarm("B0")
    # window
    send_signal_to_sfarm("C_S-0")
    # co2
    send_signal_to_ssfarm("Y0")
    # o2
    send_signal_to_ssfarm("G1")
    # water
    send_signal_to_ssfarm("W0")
    # sound
    beepsound()

# 비 4단계
def rain_forth():
    # fan
    send_signal_to_sfarm("C_F-1")
    # heat
    send_signal_to_ssfarm("RO")
    # light
    send_signal_to_sfarm("C_L-5")
    # fog
    send_signal_to_ssfarm("B0")
    # window
    send_signal_to_sfarm("C_S-0")
    # co2
    send_signal_to_ssfarm("Y1")
    # o2
    send_signal_to_ssfarm("G0")
    # water
    send_signal_to_ssfarm("W0")
    # sound
    beepsound()

# 비 5단계
def rain_fifth():
    # fan
    send_signal_to_sfarm("C_F-1")
    # heat
    send_signal_to_ssfarm("R1")
    # light
    send_signal_to_sfarm("C_L-7")
    # fog
    send_signal_to_ssfarm("B0")
    # window
    send_signal_to_sfarm("C_S-0")
    # co2
    send_signal_to_ssfarm("Y1")
    # o2
    send_signal_to_ssfarm("G0")
    # water
    send_signal_to_ssfarm("W0")
    # sound
    beepsound()

def play():
    global msg_growth
    while True:
        # schedule 실행
        schedule.run_pending()

        # 발아 적온
        schedule.every(10).seconds.do(summer_first)
        schedule.every(10).seconds.do(winter_first)
        schedule.every(10).seconds.do(rain_first)

        # 육묘 적온
        schedule.every(10).seconds.do(summer_second)
        schedule.every(10).seconds.do(winter_second)
        schedule.every(10).seconds.do(rain_second)

        # 생육 낮 적온
        schedule.every(10).seconds.do(summer_third1)
        schedule.every(10).seconds.do(winter_third1)
        schedule.every(10).seconds.do(rain_third1)

        # 생육 밤 적온
        schedule.every(10).seconds.do(summer_third2)
        schedule.every(10).seconds.do(winter_third2)
        schedule.every(10).seconds.do(rain_third2)

        # 개화 적온
        schedule.every(10).seconds.do(summer_forth)
        schedule.every(10).seconds.do(winter_forth)
        schedule.every(10).seconds.do(rain_forth)


        # 과비대 적온
        schedule.every(10).seconds.do(summer_fifth)
        schedule.every(10).seconds.do(winter_fifth)
        schedule.every(10).seconds.do(rain_fifth)

        if keyboard.is_pressed("q"):
            break

    return msg_growth

play()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------


df = pd.read_csv("data/control_rules.csv")
df["season_level"] = df["season"] + " " + df["level"]
print(df.head())


@app.route("/msg_growth")
@cross_origin(origin='*')
def msg_growth():
    msg_growth_str = msg_growth
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

    return jsonify(resp)


app.run(host="0.0.0.0", threaded=True)



