#! /usr/bin/python

# Based on https://raw.githubusercontent.com/carolinedunn/facial_recognition/main/facial_req_email.py

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
import pathlib
import datetime
from targets import *

#Initialize 'currentname' to trigger only when a new person is identified.
currentname = "unknown"
#Determine faces from encodings.pickle file model created from train_model.py
encodingsP = pathlib.Path(__file__).parent.resolve() / "dataset" / "encodings.pickle"
#use this xml file
cascade = str(pathlib.Path(__file__).parent.resolve() / "haarcascade_frontalface_default.xml")

def send_message(name):
    # TODO: Send message to the GUI
    return


def drawText(img, text,
          fontFace=cv2.FONT_HERSHEY_PLAIN,
          bottomLeft=None,
          topLeft=None,
          fontScale=3,
          thickness=2,
          color=(0, 255, 0),
          backgroundColor=(0, 0, 0),
          padding=4
          ):

    text_size, _ = cv2.getTextSize(text, fontFace, fontScale, thickness)
    text_w, text_h = text_size
    if bottomLeft:
        left, bottom = bottomLeft
        top = bottom - text_h - padding*2
    if topLeft:
        left, top = topLeft
        bottom = top + text_h + padding*2
    cv2.rectangle(img, (left, top), (left + text_w + padding*2, top + text_h + padding*2), backgroundColor, -1)
    cv2.putText(img, text, (left + padding, top + text_h + int(fontScale) - 1 + padding), fontFace, fontScale, color, thickness)

    return text_size

# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())
detector = cv2.CascadeClassifier(cascade)

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# start the FPS counter
fps = FPS().start()

# loop over frames from the video file stream
while True:
    # grab the frame from the threaded video stream and resize it
    # to 500px (to speedup processing)
    frame = vs.read()
    # frame = imutils.resize(frame, width=1000)
    
    # convert the input frame from (1) BGR to grayscale (for face
    # detection) and (2) from BGR to RGB (for face recognition)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # detect faces in the grayscale frame
    rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
        minNeighbors=5, minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE)

    # OpenCV returns bounding box coordinates in (x, y, w, h) order
    # but we need them in (top, right, bottom, left) order, so we
    # need to do a bit of reordering
    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

    # compute the facial embeddings for each face bounding box
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []
    confidences = []

    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"],
            encoding, tolerance=0.4)
        distances = face_recognition.face_distance(data["encodings"],
            encoding)
        name = "Unknown"
        confidence = 0

        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            bestDistance = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
                if name in bestDistance.keys():
                    bestDistance[name] = min(distances[i], bestDistance[name])
                else:
                    bestDistance[name] = distances[i]

            # determine the recognized face with the largest number
            # of votes (note: in the event of an unlikely tie Python
            # will select first entry in the dictionary)
            name = min(bestDistance, key=bestDistance.get)
            confidence = 1 - bestDistance[name]
            
            #If someone in your dataset is identified, print their name on the screen
            if currentname != name:
                currentname = name
                print(f"[DETECTED PERSON] {datetime.datetime.now()} - {nameForTarget[name]}")
                #Take a picture to send in the email
                # img_name = "image.jpg"
                # cv2.imwrite(img_name, frame)
                # print('Taking a picture.')
                
                #Now send me an email to let me know who is at the door
                request = send_message(name)
                # print ('Status Code: '+format(request.status_code)) #200 status code means email sent successfully
                
        # update the list of names
        names.append(name)
        confidences.append(confidence)

    # loop over the recognized faces
    for ((top, right, bottom, left), name, confidence) in zip(boxes, names, confidences):
        # draw the predicted face name on the image - color is in BGR
        cv2.rectangle(frame, (left, top), (right, bottom),
            (112, 37, 87), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        # f"({numberForTarget[name]}) {nameForTarget[name]}",
        if confidence > 0:
            text = f"{confidence * 100 :.2f}% {nameForTarget[name]}"
        else:
            text = "Unknown"
        drawText(img=frame,
                text=text, 
          bottomLeft=(left, top), 
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
           fontScale=0.8, 
               color=(255, 255, 255),
     backgroundColor=(112, 37, 87),
           thickness=2)

    # display the image to our screen
    window = "ECAI Target Detector"
    cv2.namedWindow(window, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window, cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow(window, frame)
    key = cv2.waitKey(1) & 0xFF

    # if the ESC key was pressed, break from the loop
    if key == 27:
        break

    # update the FPS counter
    fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
