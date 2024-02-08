# SPDX-License-Identifier: GPL-3.0-or-later

import cv2
import numpy as np
import sys
import pathlib
import os

# print(cv2.__file__)

cap = cv2.VideoCapture(0)

username = sys.argv[1]
fullname = sys.argv[2]

datasetPath = pathlib.Path(__file__).parent.resolve() / "dataset" / username

os.makedirs(datasetPath, exist_ok=True)

imageCountFilePath = datasetPath / f"imageCount.txt"
try:
    with open(imageCountFilePath) as imageCountFile:
        imageCounter = int(imageCountFile.readline())
except:
    imageCounter = 0


while cap.isOpened():
    status, frame = cap.read()
    key = cv2.waitKey(1)
    if key == 27: # ESC key
        break
    elif key == 32: # SPACE key
        imagePath = str(datasetPath / f"image_{imageCounter}.jpg")
        cv2.imwrite(imagePath, frame)
        print(f"{imagePath} written!")
        imageCounter += 1

    cv2.imshow(f"Headshot for {fullname} - SPACE take picture - ESC exit", frame)

with open(imageCountFilePath, "w") as imageCountFile:
    imageCountFile.write(str(imageCounter) + "\n")
