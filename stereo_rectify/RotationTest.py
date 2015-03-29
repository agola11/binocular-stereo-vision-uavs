import cv2
import numpy as np
from time import sleep

# Rotation-based image rectification for a single eye

fname = "c:\\Users\\Joseph\Videos\\RightNoFish.avi"

F = np.array([[1.21710707e+03,   0.00000000e+00,   1.36923928e+03],
              [0.00000000e+00,   1.22282317e+03,   9.78605574e+02],
              [0.00000000e+00,   0.00000000e+00,   1.00000000e+00]])
dist = np.array([[ -3.19826380e-01,   1.74633694e-01,   2.05930039e-04,   2.01208997e-04, -8.69545436e-02]] )

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
    th = np.pi/10.
    R = np.array([[1, 0, 0],
                  [0, np.cos(th), -np.sin(th)],
                  [0, np.sin(th), np.cos(th)]])
    K = F.dot(R.dot(np.linalg.inv(F)))
    #R = np.array([[1.,0,0],
    #              [0,1.,0],
    #              [0,0,1.]])
    print K
    print frame.shape
    newframe = cv2.undistort(frame, F, dist)
    #newframe = cv2.warpPerspective(frame,K,(1280,960))
    cv2.imshow(new_window,newframe)
    cv2.waitKey(30)