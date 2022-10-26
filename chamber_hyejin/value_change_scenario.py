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

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def send_signal_to_sfarm(msg):
    url = f'http://localhost:5000/send_signal_sfarm'
    requests.post(url, json={"msg": msg})
    # pass

def send_signal_to_ssfarm(msg):
    url = f'http://localhost:5000/send_signal_ssfarm'
    requests.post(url, json={"msg": msg})


def beepsound():
    freq = 2000    # range : 37 ~ 32767
    dur = 150    # ms
    ws.Beep(freq, dur) # winsound.Beep(frequency, duration)


def set_message(msg):
    url = f'http://localhost:5000/set_scenario'
    requests.post(url, json={"msg": msg})


# 여름 1단계
def summer_first():
    set_message("여름 1단계")
    # fan
    send_signal_to_ssfarm("C_F-0")
    # heat
    send_signal_to_ssfarm("RO")
    # light
    send_signal_to_sfarm("C_L-9")
    # fog
    send_signal_to_ssfarm("B0")
    # window
    send_signal_to_ssfarm("C_S-1")
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
    set_message("여름 2단계")

    # fan
    send_signal_to_ssfarm("C_F-1")
    # heat
    send_signal_to_ssfarm("RO")
    # light
    send_signal_to_sfarm("C_L-6")
    # fog
    send_signal_to_ssfarm("B0")
    # window
    send_signal_to_ssfarm("C_S-1")
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
    set_message("여름 3-1단계")

    # fan
    send_signal_to_ssfarm("C_F-1")
    # heat
    send_signal_to_sfarm("RO")
    # light
    send_signal_to_sfarm("C_L-7")
    # fog
    send_signal_to_ssfarm("B0")
    # window
    send_signal_to_ssfarm("C_S-1")
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
    set_message("여름 3-2단계")

    # fan
    send_signal_to_ssfarm("C_F-1")
    # heat
    send_signal_to_ssfarm("RO")
    # light
    send_signal_to_sfarm("C_L-0")
    # fog
    send_signal_to_ssfarm("B0")
    # window
    send_signal_to_ssfarm("C_S-1")
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
    set_message("여름 4단계")

    # fan
    send_signal_to_ssfarm("C_F-1")
    # heat
    send_signal_to_ssfarm("RO")
    # light
    send_signal_to_sfarm("C_L-5")
    # fog
    send_signal_to_ssfarm("B0")
    # window
    send_signal_to_ssfarm("C_S-1")
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
    set_message("여름 5단계")

    # fan
    send_signal_to_ssfarm("C_F-1")
    # heat
    send_signal_to_ssfarm("RO")
    # light
    send_signal_to_sfarm("C_L-8")
    # fog
    send_signal_to_ssfarm("B0")
    # window
    send_signal_to_ssfarm("C_S-1")
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
    set_message("겨울 1단계")

    # fan
    send_signal_to_ssfarm("C_F-1")
    # heat
    send_signal_to_ssfarm("R1")
    # light
    send_signal_to_sfarm("C_L-9")
    # fog
    send_signal_to_ssfarm("B1")
    # window
    send_signal_to_ssfarm("C_S-0")
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
    set_message("겨울 2단계")

    # fan
    send_signal_to_ssfarm("C_F-0")
    # heat
    send_signal_to_ssfarm("R1")
    # light
    send_signal_to_sfarm("C_L-9")
    # fog
    send_signal_to_ssfarm("B1")
    # window
    send_signal_to_ssfarm("C_S-0")
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
    set_message("겨울 3-1단계")

    # fan
    send_signal_to_ssfarm("C_F-0")
    # heat
    send_signal_to_ssfarm("R1")
    # light
    send_signal_to_sfarm("C_L-7")
    # fog
    send_signal_to_ssfarm("B1")
    # window
    send_signal_to_ssfarm("C_S-1")
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
    set_message("겨울 3-2단계")

    # fan
    send_signal_to_ssfarm("C_F-0")
    # heat
    send_signal_to_ssfarm("R1")
    # light
    send_signal_to_sfarm("C_L-0")
    # fog
    send_signal_to_ssfarm("B1")
    # window
    send_signal_to_ssfarm("C_S-0")
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
    set_message("겨울 4단계")

    # fan
    send_signal_to_ssfarm("C_F-0")
    # heat
    send_signal_to_ssfarm("R1")
    # light
    send_signal_to_sfarm("C_L-6")
    # fog
    send_signal_to_ssfarm("B1")
    # window
    send_signal_to_ssfarm("C_S-0")
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
    set_message("겨울 5단계")

    # fan
    send_signal_to_ssfarm("C_F-0")
    # heat
    send_signal_to_ssfarm("R1")
    # light
    send_signal_to_sfarm("C_L-8")
    # fog
    send_signal_to_ssfarm("B1")
    # window
    send_signal_to_ssfarm("C_S-0")
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
    set_message("비 1단계")

    # fan
    send_signal_to_ssfarm("C_F-1")
    # heat
    send_signal_to_ssfarm("R1")
    # light
    send_signal_to_sfarm("C_L-9")
    # fog
    send_signal_to_ssfarm("B0")
    # window
    send_signal_to_ssfarm("C_S-0")
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
    set_message("비 2단계")

    # fan
    send_signal_to_ssfarm("C_F-1")
    # heat
    send_signal_to_ssfarm("RO")
    # light
    send_signal_to_sfarm("C_L-7")
    # fog
    send_signal_to_ssfarm("B0")
    # window
    send_signal_to_ssfarm("C_S-0")
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
    set_message("비 3-1단계")

    # fan
    send_signal_to_ssfarm("C_F-1")
    # heat
    send_signal_to_ssfarm("R1")
    # light
    send_signal_to_sfarm("C_L-6")
    # fog
    send_signal_to_ssfarm("B0")
    # window
    send_signal_to_ssfarm("C_S-0")
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
    set_message("비 3-2단계")

    # fan
    send_signal_to_ssfarm("C_F-1")
    # heat
    send_signal_to_ssfarm("RO")
    # light
    send_signal_to_sfarm("C_L-0")
    # fog
    send_signal_to_ssfarm("B0")
    # window
    send_signal_to_ssfarm("C_S-0")
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
    set_message("비 4단계")

    # fan
    send_signal_to_ssfarm("C_F-1")
    # heat
    send_signal_to_ssfarm("RO")
    # light
    send_signal_to_sfarm("C_L-5")
    # fog
    send_signal_to_ssfarm("B0")
    # window
    send_signal_to_ssfarm("C_S-0")
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
    set_message("비 5단계")

    # fan
    send_signal_to_ssfarm("C_F-1")
    # heat
    send_signal_to_ssfarm("R1")
    # light
    send_signal_to_ssfarm("C_L-7")
    # fog
    send_signal_to_ssfarm("B0")
    # window
    send_signal_to_ssfarm("C_S-0")
    # co2
    send_signal_to_ssfarm("Y1")
    # o2
    send_signal_to_ssfarm("G0")
    # water
    send_signal_to_ssfarm("W0")
    # sound
    beepsound()

def play():
    while True:
        print("sce:summer-1")
        summer_first()
        time.sleep(5)
        print("sce:winter-1")
        winter_first()
        time.sleep(5)
        print("sce:rain-1")
        rain_first()
        time.sleep(5)
        print("sce:summer-2")
        summer_second()
        time.sleep(10)
        print("sce:winter-2")
        winter_second()
        time.sleep(10)
        print("sce:rain-2")
        rain_second()
        time.sleep(10)

        if keyboard.is_pressed("q"):
            break
play()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------



