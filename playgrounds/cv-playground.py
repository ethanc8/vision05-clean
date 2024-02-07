# SPDX-License-Identifier: GPL-3.0-or-later

import cv2
import numpy as np

# print(cv2.__file__)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    status, image = cap.read()
    key = cv2.waitKey(1)
    if key == 27: # ESC key
        break

    cv2.imshow("SCAI Target Detector", image)