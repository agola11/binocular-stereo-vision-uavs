#!/usr/bin/python

import cv2
import numpy as np
"""
H_LOW = 21, S_LOW = 95, V_LOW = 97
H_HI = 40, S_HI = 180, V_HI = 255
"""
"""
H_LOW = 25, S_LOW = 95, V_LOW = 93
H_HI = 38, S_HI = 212, V_HI = 255
"""
"""
LOW LIGHTING
H_LOW = 29, S_LOW = 123, V_LOW = 32
H_HI = 39, S_HI = 255, V_HI = 248
SMOOTH=15
"""
"""
RED
H_LOW = 173, S_LOW = 175, V_LOW = 94
H_HI = 179, S_HI = 255, V_HI = 197
SMOOTH=1
"""

"""
PINK BALL
HSV_Lo = 127,98, 118
HSV_HI = 178, 255, 255
SMOOTH=1
"""

"""
PINK BALL INDOORS C920
H_LOW = 173, S_LOW = 77, V_LOW = 146
H_HI = 191, S_HI = 255, V_HI = 255
SMOOTH=1
"""
"""
OUTISDE LAB PINK BALL C920
H_LOW = 175, S_LOW = 68, V_LOW = 126
H_HI = 185, S_HI = 255, V_HI = 247
SMOOTH=1
"""
cap = cv2.VideoCapture(0)

def nothing(x):
    pass
# Creating a window for later use
cv2.namedWindow('result')

# Starting with 100's to prevent error while masking
h,s,v = 100,100,100

# Creating track bar
cv2.createTrackbar('h_low', 'result',0,255,nothing)
cv2.createTrackbar('s_low', 'result',0,255,nothing)
cv2.createTrackbar('v_low', 'result',0,255,nothing)

cv2.createTrackbar('h_hi', 'result',0,255,nothing)
cv2.createTrackbar('s_hi', 'result',0,255,nothing)
cv2.createTrackbar('v_hi', 'result',0,255,nothing)

cv2.createTrackbar('morph', 'result',0,1,nothing)
cv2.createTrackbar('smooth', 'result',1,15,nothing)

while(1):

    _, frame = cap.read()

    #converting to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # get info from track bar and appy to result
    h = cv2.getTrackbarPos('h_low','result')
    s = cv2.getTrackbarPos('s_low','result')
    v = cv2.getTrackbarPos('v_low','result')

    h_hi = cv2.getTrackbarPos('h_hi','result')
    s_hi = cv2.getTrackbarPos('s_hi','result')
    v_hi = cv2.getTrackbarPos('v_hi','result')

    morph = cv2.getTrackbarPos('morph','result')
    smooth = cv2.getTrackbarPos('smooth','result')

    # Normal masking algorithm
    lower_blue = np.array([h, s, v])
    upper_blue = np.array([h_hi, s_hi, v_hi])
    

    print("H_LOW = " + str(h) + ", " + "S_LOW = " + str(s) + ", " + "V_LOW = " + str(v))
    print("H_HI = " + str(h_hi) + ", " + "S_HI = " + str(s_hi) +", " + "V_HI = " + str(v_hi))

    mask = cv2.inRange(hsv,lower_blue, upper_blue)


    if morph:
        # Do Dilation and Erosion
        kernel_close = np.ones((21,21),np.uint8)
        kernel_open = np.ones((11, 11), np.uint8)
        kernel_erode = np.ones((4, 4), np.uint8)
        kernel_dilate = np.ones((8, 8), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_close)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open)
        #mask = cv2.erode(mask, kernel_erode, iterations=2)
        #mask = cv2.dilate(mask, kernel_dilate, iterations=2)

    print ("SMOOTH=" + str(smooth))
    mask = cv2.GaussianBlur(mask,(15,15),0)

    circles = cv2.HoughCircles(mask,cv2.cv.CV_HOUGH_GRADIENT,1,1600, param1 = 50, param2 = 22)
    result = cv2.bitwise_and(frame,frame,mask = mask)

    if circles != None:
    	print circles
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(result,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(result,(i[0],i[1]),2,(0,0,255),3)
            print (i[0], i[1])

    res = cv2.resize(result,None,fx=0.5, fy=0.5)
    cv2.imshow('result',res)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()