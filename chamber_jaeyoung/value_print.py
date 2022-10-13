import time
import schedule
import serial
import json
import keyboard

s = serial.Serial('COM3', 9600)

# 아두이노로 신호 송신
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


# 여름 1단계
def summer_first():
    # fan
    send_signal_to_sfarm("C_F-0")
    # heat
    send_signal_to_sfarm("RO")
    # light
    send_signal_to_sfarm("C_L-9")
    # fog
    send_signal_to_sfarm("B0")
    # window
    send_signal_to_sfarm("S1")

# 여름 2단계
def summer_second():
    # fan
    send_signal_to_sfarm("C_F-1")
    # heat
    send_signal_to_sfarm("RO")
    # light
    send_signal_to_sfarm("C_L-6")
    # fog
    send_signal_to_sfarm("B0")
    # window
    send_signal_to_sfarm("S1")


# 여름 3-1단계
def summer_third1():
    # fan
    send_signal_to_sfarm("C_F-1")
    # heat
    send_signal_to_sfarm("RO")
    # light
    send_signal_to_sfarm("C_L-7")
    # fog
    send_signal_to_sfarm("B0")
    # window
    send_signal_to_sfarm("S1")

# 여름 3-2단계
def summer_third2():
    # fan
    send_signal_to_sfarm("C_F-1")
    # heat
    send_signal_to_sfarm("RO")
    # light
    send_signal_to_sfarm("C_L-0")
    # fog
    send_signal_to_sfarm("B0")
    # window
    send_signal_to_sfarm("S1")

# 여름 4단계
def summer_forth():
    # fan
    send_signal_to_sfarm("C_F-1")
    # heat
    send_signal_to_sfarm("RO")
    # light
    send_signal_to_sfarm("C_L-5")
    # fog
    send_signal_to_sfarm("B0")
    # window
    send_signal_to_sfarm("S1")

# 여름 5단계
def summer_fifth():
    # fan
    send_signal_to_sfarm("C_F-1")
    # heat
    send_signal_to_sfarm("RO")
    # light
    send_signal_to_sfarm("C_L-8")
    # fog
    send_signal_to_sfarm("B0")
    # window
    send_signal_to_sfarm("S1")

# 겨울 1단계
def winter_first():
    # fan
    send_signal_to_sfarm("C_F-1")
    # heat
    send_signal_to_sfarm("R1")
    # light
    send_signal_to_sfarm("C_L-9")
    # fog
    send_signal_to_sfarm("B1")
    # window
    send_signal_to_sfarm("S0")

# 겨울 2단계
def winter_second():
    # fan
    send_signal_to_sfarm("C_F-0")
    # heat
    send_signal_to_sfarm("R1")
    # light
    send_signal_to_sfarm("C_L-9")
    # fog
    send_signal_to_sfarm("B1")
    # window
    send_signal_to_sfarm("S0")

# 겨울 3-1단계
def winter_third1():
    # fan
    send_signal_to_sfarm("C_F-0")
    # heat
    send_signal_to_sfarm("R1")
    # light
    send_signal_to_sfarm("C_L-7")
    # fog
    send_signal_to_sfarm("B1")
    # window
    send_signal_to_sfarm("S1")

# 겨울 3-2단계
def winter_third2():
    # fan
    send_signal_to_sfarm("C_F-0")
    # heat
    send_signal_to_sfarm("R1")
    # light
    send_signal_to_sfarm("C_L-0")
    # fog
    send_signal_to_sfarm("B1")
    # window
    send_signal_to_sfarm("S0")

# 겨울 4단계
def winter_forth():
    # fan
    send_signal_to_sfarm("C_F-0")
    # heat
    send_signal_to_sfarm("R1")
    # light
    send_signal_to_sfarm("C_L-6")
    # fog
    send_signal_to_sfarm("B1")
    # window
    send_signal_to_sfarm("S0")

# 겨울 5단계
def winter_fifth():
    # fan
    send_signal_to_sfarm("C_F-0")
    # heat
    send_signal_to_sfarm("R1")
    # light
    send_signal_to_sfarm("C_L-8")
    # fog
    send_signal_to_sfarm("B1")
    # window
    send_signal_to_sfarm("S0")

# 비 1단계
def rain_first():
    # fan
    send_signal_to_sfarm("C_F-1")
    # heat
    send_signal_to_sfarm("R1")
    # light
    send_signal_to_sfarm("C_L-9")
    # fog
    send_signal_to_sfarm("B0")
    # window
    send_signal_to_sfarm("S0")

# 비 2단계
def rain_second():
    # fan
    send_signal_to_sfarm("C_F-1")
    # heat
    send_signal_to_sfarm("RO")
    # light
    send_signal_to_sfarm("C_L-7")
    # fog
    send_signal_to_sfarm("B0")
    # window
    send_signal_to_sfarm("S0")

# 비 3-1단계
def rain_third1():
    # fan
    send_signal_to_sfarm("C_F-1")
    # heat
    send_signal_to_sfarm("R1")
    # light
    send_signal_to_sfarm("C_L-6")
    # fog
    send_signal_to_sfarm("B0")
    # window
    send_signal_to_sfarm("S0")

# 비 3-2단계
def rain_third2():
    # fan
    send_signal_to_sfarm("C_F-1")
    # heat
    send_signal_to_sfarm("RO")
    # light
    send_signal_to_sfarm("C_L-0")
    # fog
    send_signal_to_sfarm("B0")
    # window
    send_signal_to_sfarm("S0")

# 비 4단계
def rain_forth():
    # fan
    send_signal_to_sfarm("C_F-1")
    # heat
    send_signal_to_sfarm("RO")
    # light
    send_signal_to_sfarm("C_L-5")
    # fog
    send_signal_to_sfarm("B0")
    # window
    send_signal_to_sfarm("S0")

# 비 5단계
def rain_fifth():
    # fan
    send_signal_to_sfarm("C_F-1")
    # heat
    send_signal_to_sfarm("R1")
    # light
    send_signal_to_sfarm("C_L-7")
    # fog
    send_signal_to_sfarm("B0")
    # window
    send_signal_to_sfarm("S0")


# 초 단위로 실행
while True:
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

    if keyborad.is_pressed("q"):
        break
