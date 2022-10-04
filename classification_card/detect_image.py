import tensorflow as tf
import numpy as np
import time
import cv2
import datetime
import schedule

def take_picture():
    # Current time
    now = datetime.datetime.now().strftime("%d_%H-%M-%S")

    # Define the input size of the model
    input_size = (224, 224)

    # Open the web cam
    cap = cv2.VideoCapture(0)  # webcam 불러오기
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 5)

    # Load the saved model
    model = tf.keras.models.load_model("keras_model.h5", compile=False)

    while cap.isOpened():

        # Reading frames from the camera
        ret, frame = cap.read()
        if not ret:
            break

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

        cv2.putText(frame, now, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (225, 0, 0), thickness=1)
        cv2.putText(frame, msg_card, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 2, (225, 0, 0), thickness=2)

        if ret:
            # Show the result and frame
            cv2.imshow('classification_card', frame)
            # Save the current time as the title
            cv2.imwrite(f'../classification_card/image_data/{now}.jpg', frame)
            break

def main():
    # Take a picture at 10:30 every day
    schedule.every().day.at("10:30").do(take_picture)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()