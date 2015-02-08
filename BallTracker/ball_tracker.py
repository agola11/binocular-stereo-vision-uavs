import cv2
import time, sys, os
import numpy as np

# read in the image
scene = cv2.imread("./still_imgs/tennis.jpg")

hsv_img = cv2.cvtColor(scene, cv2.COLOR_BGR2HSV)

lower_green = np.array([36,int(0.76 * 255), int(0.76 * 255)])
upper_green = np.array([45,255, 255])

# Threshold the HSV image to get only blue colors
frame_threshed = cv2.inRange(hsv_img, lower_green, upper_green)
cv2.imwrite('output2.jpg', frame_threshed)


