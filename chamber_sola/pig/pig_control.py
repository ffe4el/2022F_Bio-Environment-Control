import serial

s = serial.Serial('COM9', 9600)

def send_signal_to_sfarm(msg):
    if (s.readable()):
        s.write("{}\n".format(msg).encode())


def red_on():
    send_signal_to_sfarm("R1")
    # print("fan on")
    # return "Order Fan On"