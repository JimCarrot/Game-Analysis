from builtins import str

from keras.preprocessing.image import img_to_array
import imutils
from datetime import date, datetime
import cv2
from keras.models import load_model
import numpy as np
import json


class real_time_vid:
    # parameters for loading data and images
    detection_model_path = 'haarcascade_files/haarcascade_frontalface_default.xml'
    emotion_model_path = 'models/_mini_XCEPTION.102-0.66.hdf5'

    # hyper-parameters for bounding boxes shape
    # loading models
    face_detection = cv2.CascadeClassifier(detection_model_path)
    emotion_classifier = load_model(emotion_model_path, compile=False)
    EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised",
                "neutral"]

    # Getting the current date and time then adding both variables to the facial_expression dictionary
    today = "{0}-{1}-{2}".format(str(date.today().year), str(date.today().month), str(date.today().day))
    currentTime = "{0}:{1}:{2}".format(datetime.now().hour, datetime.now().minute, datetime.now().second)

    # Initialising the facial_expression dictionary
    facial_expressions = {
        'startDate': today,
    }
    facialExpressions = ""
    # feelings_faces = []
    # for index, emotion in enumerate(EMOTIONS):
    # feelings_faces.append(cv2.imread('emojis/' + emotion + '.png', -1))

    # starting video streaming
    # cv2.namedWindow('your_face')
    camera = cv2.VideoCapture(2)
    operating = True

    # Starting while loop that will go over each frame that is being recorded through the webcam
    while True:
        if operating:
            # Getting the start time of the facial recognition
            facial_expressions["startTime"] = currentTime
            operating = False
            print("Current Time has been added")

        frame = camera.read()[1]
        # reading the frame
        frame = imutils.resize(frame, width=300)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detection.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                                flags=cv2.CASCADE_SCALE_IMAGE)

        canvas = np.zeros((250, 300, 3), dtype="uint8")
        frameClone = frame.copy()
        if len(faces) > 0:
            faces = sorted(faces, reverse=True,
                           key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
            (fX, fY, fW, fH) = faces
            # Extract the ROI of the face from the grayscale image, resize it to a fixed 28x28 pixels, and then prepare
            # the ROI for classification via the CNN
            roi = gray[fY:fY + fH, fX:fX + fW]
            roi = cv2.resize(roi, (64, 64))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            # Getting the prediction rating and emotion labels
            preds = emotion_classifier.predict(roi)[0]
            emotion_probability = np.max(preds)
            label = EMOTIONS[preds.argmax()]

            # Getting the variables associated to emotions

            # Timestamp of the frame currently being read
            currentFrame = "{0}:{1}:{2}".format(datetime.now().hour, datetime.now().minute, datetime.now().second)
            expression = "" + currentFrame + "/"
            first = True
            for i in range(len(EMOTIONS)):
                if first:
                    prediction = preds[i].item()
                    expression += str(prediction)
                    first = False
                else:
                    prediction = preds[i].item()
                    expression += "-" + str(prediction)

            expression += ","
            # Adding current emotion readings to the facialExpression array inside of the facial_expression dictionary
            facialExpressions += expression


        else:
            continue

        for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
            # construct the label text
            text = "{}: {:.2f}%".format(emotion, prob * 100)

            # draw the label + probability bar on the canvas
            # emoji_face = feelings_faces[np.argmax(preds)]

            w = int(prob * 300)
            cv2.rectangle(canvas, (7, (i * 35) + 5),
                          (w, (i * 35) + 35), (0, 0, 255), -1)
            cv2.putText(canvas, text, (10, (i * 35) + 23),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                        (255, 255, 255), 2)
            cv2.putText(frameClone, label, (fX, fY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            cv2.rectangle(frameClone, (fX, fY), (fX + fW, fY + fH),
                          (0, 0, 255), 2)
        #    for c in range(0, 3):
        #        frame[200:320, 10:130, c] = emoji_face[:, :, c] * \
        #        (emoji_face[:, :, 3] / 255.0) + frame[200:320,
        #        10:130, c] * (1.0 - emoji_face[:, :, 3] / 255.0)

        # cv2.imshow('your_face', frameClone)
        cv2.imshow("Probabilities", canvas)

        # Waiting for the 'Q' key to be pressed.
        # Once pressed the endtime will be logged and then added to the dictionary
        if cv2.waitKey(1) & 0xFF == ord('q'):
            facialList = facialExpressions.split(",")
            index = 1
            fileIndex = 0
            facialString = ""
            for face in facialList:
                if index % 26 == 0:
                    facial_expressions["endTime"] = "{0}:{1}:{2}".format(datetime.now().hour,
                                                                         datetime.now().minute,
                                                                         datetime.now().second)
                    facial_expressions["nameSpace"] = "facialexpression.com"
                    facial_expressions["name"] = "facialExpressionEvent"
                    facial_expressions["version"] = "0.0.1"
                    facial_expressions["facialExpressions"] = facialString
                    with open('../../../ApexFiles/event/facialRecog/EventIn_FacialExpressions' + str(fileIndex) + '.json',
                              'w') as fp:
                        json.dump(facial_expressions, fp)
                    index = 1
                    fileIndex+=1
                    facialString = ""
                else:
                    index += 1
                    facialString += face + ","
            break

    camera.release()
    cv2.destroyAllWindows()
