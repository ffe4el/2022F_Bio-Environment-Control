import cv2
import numpy as np
from urllib.request import urlopen
import tensorflow as tf


url = "http://192.168.0.12/stream"  # ESP CAM의 영상 스트리밍 주소
stream = urlopen(url)
buffer = b''


# Define the input size of the model
input_size = (224, 224)

# Open the web cam
cap = cv2.VideoCapture(0) # webcam 불러오기
cap.set(cv2.CAP_PROP_BUFFERSIZE, 5)

# Load the saved model
model = tf.keras.models.load_model("keras_model.h5", compile=False)


while True:
    buffer += stream.read(4096)
    head = buffer.find(b'\xff\xd8')
    end = buffer.find(b'\xff\xd9')
    try:  # 가끔 비어있는 버퍼를 받아 오류가 발생함. 이를 위한 try문
        if head > -1 and end > -1:
            jpg = buffer[head:end + 2]
            buffer = buffer[end + 2:]
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            cv2.imshow("stream", frame)
            key = cv2.waitKey(1)
    except:
        pass

    # Resize the frame for the model
    model_frame = cv2.resize(frame, input_size, frame)
    # Expand Dimension (224, 224, 3) -> (1, 224, 224, 3) and Nomarlize the data
    model_frame = np.expand_dims(model_frame, axis=0) / 255.0

    # Predict
    is_card_prob = model.predict(model_frame)[0]
    is_card = np.argmax(is_card_prob)

    # Add Information on screen
    if is_card == 0:
        msg_card = "Card 1"
    elif is_card == 1:
        msg_card = "Card 2"
    elif is_card == 2:
        msg_card = "Card 3"
    else:
        msg_card = "It's not card"

    msg_card += " ({:.1f})%".format(is_card_prob[is_card] * 100)


    cv2.putText(frame, msg_card, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (225, 0, 0), thickness=2)

    # Show the result and frame
    cv2.imshow('classification_card', frame)

    # Press Q on keyboard to exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
