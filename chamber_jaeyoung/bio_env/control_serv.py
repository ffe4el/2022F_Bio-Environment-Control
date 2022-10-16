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
from flask_cors import cross_origin
import cv2
from urllib.request import urlopen
import tensorflow as tf
import time
import schedule
import keyboard
import winsound as ws

app = Flask(__name__)

# 10번 포트에 연결된 serial을 s로 지정(채널:9600)
# 아두이노 메가
s = serial.Serial('COM3', 9600)
#아두이노 우노
ss = serial.Serial('COM6', 9600)

# 웹에 값 표시하기
# classification msg
msg_level = "Ready"
# temperature msg
temp = "Ready"
# humid msg
humid = "Ready"
# cdc msg
cdc = "Ready"

# camera 작동 및 웹페이지로 송신
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
                    msg_level = "level 1"
                elif is_level == 1:
                    msg_level = "level 2"
                elif is_level == 2:
                    msg_level = "level 3"
                elif is_level == 3:
                    msg_level = "level 4"
                elif is_level == 4:
                    msg_level = "level 5"
                else:
                    msg_level = "No"

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

# 아두이노 메가 신호 송신 및 수신
def send_signal_to_sfarm(msg):
    while True:
        global temp
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

# 아두이노 우노로 신호 송신 및 수신
def send_signal_to_ssfarm(msg):
    if (ss.readable()):
        ss.write("{}\n".format(msg).encode())
        time.sleep(0.2)

# 이건 무슨 함수일까? 환경값 불러오기...?
def load_env():
    z = s.readline()
    z = z.decode()[:len(z) - 1]
    data = json.loads(z)
    temp = int(data["temp"])
    humid = int(data['humidity'])
    cdc = int(data['cdc'])
    print(temp, humid, cdc)
    return temp, humid, cdc

# 소리 내기
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

def scenario():
    # 초 단위로 실행
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

        # 'q' 누르면 작동 중지
        if keyboard.is_pressed("q"):
            break

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

# flask: camera
@app.route('/')
@cross_origin(origin='*')
def index():
    return Response(camera_local(), mimetype='multipart/x-mixed-replace; boundary=frame')

# flask: classification_msg
@app.route("/classfication_msg")
@cross_origin(origin='*')
def classification_msg():
    camera_local()

# flask: temperature_msg
@app.route("/temp_msg")
@cross_origin(origin='*')
def temp_msg():
    def send_signal_to_sfarm():
        while True:
            global humid
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
        yield f"{temp}"
    return Response(send_signal_to_sfarm(), mimetype='text')

# flask: humidity_msg
@app.route("/humid_msg")
@cross_origin(origin='*')
def humid_msg():
    def send_signal_to_sfarm():
        while True:
            global humid
            z = s.readline()
            # print(z)
            # 내용이 비어있지 않으면 프린트

            if not z.decode().startswith("#"):
                z = z.decode()[:len(z) - 1]
                print("내용출력:", end="")
                print(z)
                if z.startswith("{ \"humidity"):
                    data = json.loads(z)
                    humid = int(data["humidity"])
            else:
                break
        yield f"{humid}"
        # if (s.readable()):
        #     s.write("{}\n".format(msg).encode())
    return Response(send_signal_to_sfarm(), mimetype='text')

# flask: cdc_msg
@app.route("/cdc_msg")
@cross_origin(origin='*')
def cdc_msg():
    def send_signal_to_sfarm():
        while True:
            global cdc
            z = s.readline()
            # print(z)
            # 내용이 비어있지 않으면 프린트

            if not z.decode().startswith("#"):
                z = z.decode()[:len(z) - 1]
                print("내용출력:", end="")
                print(z)
                if z.startswith("{ \"cdc"):
                    data = json.loads(z)
                    cdc = int(data["cdc"])
            else:
                break
        yield f"{cdc}"
        # if (s.readable()):
        #     s.write("{}\n".format(msg).encode())
    return Response(send_signal_to_sfarm(), mimetype='text')

# flask: fan-on
@app.route('/fan-on')
def fan_on():
    send_signal_to_sfarm("C_F-1")
    load_env()
    return "Order Fan On"


# flask: fan-off
@app.route('/fan-off')
def fan_off():
    send_signal_to_sfarm("C_F-0")
    return "Order Fan Off"

# flask: light-on
@app.route('/light-on/<level>')
def light_on(level):
    send_signal_to_sfarm("C_L-{}".format(level))
    return f"Order Light {level}"

# @app.route('/light-on')
# def light_on():
#     send_signal_to_sfarm("C_L-10")
#     return "Order Light 10"

# flask: light-off
@app.route('/light-off')
def light_off():
    send_signal_to_sfarm("C_L-0")
    return "Order Light 0"

# flask: window-open
@app.route('/window-open')
def window_open():
    send_signal_to_sfarm("C_S-1")
    return "Order window open"

# flask: window-close
@app.route('/window-close')
def window_close():
    send_signal_to_sfarm("C_S-0")
    return "Order window close"

# main함수
def main():
    app.run(host="0.0.0.0", threaded=True)
    scenario()

if __name__ == '__main__':
    main()