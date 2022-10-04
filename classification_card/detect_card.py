import tensorflow as tf
import numpy as np
import time
import schedule
import cv2
import datetime




def main():
    # Define the input size of the model
    input_size = (224, 224)

    # Open the web cam
    cap = cv2.VideoCapture(0) # webcam 불러오기
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 5)

    # Load the saved model
    model = tf.keras.models.load_model("keras_model.h5", compile=False)
    while cap.isOpened():
        # Set time before model inference
        start_time = time.time()

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

        # Compute the model inference time
        inference_time = time.time() - start_time
        fps = 1 / inference_time
        fps_msg = "Time: {:05.1f}ms {:.1f} FPS".format(inference_time * 1000, fps)

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


        cv2.putText(frame, fps_msg, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (225, 0, 0), thickness=1)
        cv2.putText(frame, msg_card, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 2, (225, 0, 0), thickness=2)

        # Show the result and frame
        cv2.imshow('classification_card', frame)

        # Press Q on keyboard to exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()