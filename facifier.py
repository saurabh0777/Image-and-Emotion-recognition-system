import cv2
import numpy as np
import os.path
import time
from cv2 import WINDOW_NORMAL
from src.face_detection import find_faces
from src.face_detection import facial_storage
from src.Face_Training_Main import Trainner
from camera import VideoCamera
from flask import Flask, render_template, Response , request


fisher_face_emotion = cv2.face.FisherFaceRecognizer_create()
fisher_face_emotion.read('models/emotion_classifier_model.xml')

fisher_face_gender = cv2.face.FisherFaceRecognizer_create()
fisher_face_gender.read('models/gender_classifier_model.xml')

emotions = ["afraid", "angry", "disgusted", "happy", "neutral", "sad", "surprised"]

ESC = 27


def trigger(firstname):
    # choice = input("Use webcam?(y/n) ")
    print ("INSIDE TRIGGER " + firstname)
    choice='y'
    if (choice == 'y'):
        # visitor_registration = input("For New Visitor registration?(y/n) ")
        if (firstname != ''):
            #face_id = input('Enter name ')
            face_id = firstname
            namecheck(face_id.lower())
            Names = read_text("Visitors.txt")
            idx = Names.index(face_id.lower())
            print("Please look to the camera for registration")
            facial_storage(idx)
            print("Preparing data...")
            faces, ids = Trainner()
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.train(faces, np.array(ids))
            recognizer.write('models/trainer.yml')
            print("Total faces trained : ", len(faces))

        predict()

    elif (choice == 'n'):
        run_loop = True
        window_name = "Facifier Static (press ESC to exit)"
        print("Type q or quit to end program")
        while run_loop:
            path = '../data/Analyze_picture/'
            file_name = input("Specify image file: ")
            if file_name == "q" or file_name == "quit":
                run_loop = False
            else:
                path += file_name + ".jpg"
                print(path)
                if os.path.isfile(path):
                    analyze_picture(fisher_face_emotion, fisher_face_gender, path, window_size=(1280, 720),
                                    window_name=window_name)
                else:
                    print("File not found!")
    else:
        print("Invalid input, exiting program.")


def namecheck(face_id):
    with open('Visitors.txt', 'r+') as fh:
        lines = fh.readlines()
        for line in lines:
            if line.startswith(face_id):
                break
        else:
            fh.write('\n' + face_id)


def read_text(file_name):
    file_data = []
    text_file = open(file_name, "r")
    for word in text_file.read().split():
        file_data.append(word)

    text_file.close()
    return file_data


def predict():
    print("Predicting image...")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('models/trainer.yml')
    font = cv2.FONT_HERSHEY_SIMPLEX
    Names = read_text("Visitors.txt")
    print(Names)
    # cam = cv2.VideoCapture(1+ cv2.CAP_DSHOW)
    cam = video_feed()
    print("cam is..",cam)
    cam.set(3, 1280)
    cam.set(4, 720)

    while (cam.isOpened()):
        ret, img = cam.read()
        # print("camera status",cam.isOpened())
        while ret == False:
            time.sleep(2)
            cam = video_feed()
            ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        for normalized_face, (x, y, w, h) in find_faces(img):
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            emotion_prediction = fisher_face_emotion.predict(normalized_face)
            if (confidence < 100):
                id = Names[id]
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))

            cv2.putText(img, str(id), (x + 5, y - 50), font, 1, (255, 255, 255), 2)
            cv2.putText(img, emotions[emotion_prediction[0]], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                        (255, 0, 0), 2)
            cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
            cv2.putText(img, "Total Visitor Count:" + str(len(Names)-1), (5, img.shape[0] - 10),
                        cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Prediction', img)
        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break
    print("Prediction completed")
    cam.release()
    cv2.destroyAllWindows()


def analyze_picture(model_emotion, model_gender, path, window_size, window_name='static'):
    cv2.namedWindow(window_name, WINDOW_NORMAL)
    cv2.namedWindow(window_name, WINDOW_NORMAL)
    if window_size:
        width, height = window_size
        cv2.resizeWindow(window_name, width, height)

    image = cv2.imread(path, 1)
    for normalized_face, (x, y, w, h) in find_faces(image):
        emotion_prediction = model_emotion.predict(normalized_face)
        gender_prediction = model_gender.predict(normalized_face)
        if (gender_prediction[0] == 0):
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        else:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(image, emotions[emotion_prediction[0]], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.imshow(window_name, image)
    key = cv2.waitKey(0)
    if key == ESC:
        cv2.destroyWindow(window_name)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


'''
print("Welcome to the Face Recogniser")

while True:
    MM = input("Press Enter to continue or end to close...")
    if MM == "end":
        break
    else:
        trigger()
'''