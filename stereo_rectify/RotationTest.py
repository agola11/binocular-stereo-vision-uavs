import cv2
import numpy as np
from time import sleep

# Rotation-based image rectification for a single eye

fname = "c:\\Users\\Joseph\Videos\\RightNoFish.avi"

orig_window = "Original Video"
new_window = "Adjusted Video"
# Open Video for Reading
cap = cv2.VideoCapture(fname)
if(not cap.isOpened()):
    print "Cannot open file"
    print fname
    quit()

cv2.namedWindow(orig_window,cv2.WINDOW_AUTOSIZE)
cv2.namedWindow(new_window,cv2.WINDOW_AUTOSIZE)

while(True):
    retval,frame = cap.read()
    if(not retval):
        break
    cv2.imshow(orig_window,frame)
    
    # Rotation!
    th = np.pi/100.
    R = np.array([[1, 0, 0],
                  [0, np.cos(th), -np.sin(th)],
                  [0, np.sin(th), np.cos(th)]])
    #R = np.array([[1.,0,0],
    #              [0,1.,0],
    #              [0,0,1.]])
    print R
    print frame.shape
    newframe = cv2.warpPerspective(frame,R,(1280,960))
    cv2.imshow(new_window,newframe)
    cv2.waitKey(30)