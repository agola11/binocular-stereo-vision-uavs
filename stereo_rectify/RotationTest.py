import cv2
import numpy as np
from time import sleep
import log_reader as lr

# Rotation-based image rectification for a single eye

# TODO For this module:
# Correct for camera distortions before rotation, and 
#       reapply barrel distortion afterwards
# Correct yaw measurements for camera pitch
# Increase sampling rate for attitude data
# Port to a callable interface


#fname = "c:\\Users\\Joseph\Videos\\FlightWithTelem.MP4"
#first_data_frame = 1712     # First frame with valid image data
#rect_start_frame = 4250     # Index of frame to start rectifying at

# Disarm occurs 225000 ms into video
# This corresponds to pixhawk time 217450
# we have data starting at pixhawk time 84612
# This corresponds to video time 92162
# this is frame 2765
#fname = "c:\\Users\\Joseph\Videos\\2015-04-07 23-51-23 3.MP4"
#rect_start_frame = 4000
#first_data_frame = 2765
fname = "c:\\Users\\Joseph\Videos\\2015-04-07 23-51-23 3.MP4"
rect_start_frame = 2240
first_data_frame = 310

F = np.array([[  2.99437818e+03,   0.00000000e+00,   9.64952231e+02],
              [  0.00000000e+00,   2.96921724e+03,   5.44881101e+02],
              [  0.00000000e+00,   0.00000000e+00,   1.00000000e+00]])
dist = np.array([[-1.71212099,  4.26268096, -0.00944359,  0.02346181, -6.42920936]] )

orig_window = "Original Video"
new_window = "Adjusted Video"

# Open video for reading
cap = cv2.VideoCapture(fname)
if(not cap.isOpened()):
    print "Cannot open video file"
    print fname
    quit()

# Fast forward to first frame with good flight data
cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, rect_start_frame)

# Calculate data start time in ms
fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
num_frames = cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
first_data_time_ms = first_data_frame*1000/fps

cv2.namedWindow(orig_window,cv2.WINDOW_AUTOSIZE)
cv2.namedWindow(new_window,cv2.WINDOW_AUTOSIZE)

#reader = lr.LogReader("attitude.log",ftype = lr.ATTITUDE_LOG_T)
reader = lr.LogReader("2015-04-07 23-51-23 3.bin.log")

while(True):
    # Read frame
    retval,frame = cap.read()
    if(not retval):
        break
    cv2.imshow(orig_window,frame[::2,::2,:])
    
    # Find index for attitude data
    now = cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
    
    # Rotation!
    print now, first_data_time_ms
    print cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
    th = ((reader.get_yaw(now-first_data_time_ms) - 287.72)/120.)
    #R = np.array([[1, 0, 0],
    #             [0, np.cos(th), -np.sin(th)],
    #             [0, np.sin(th), np.cos(th)]])
    #R = np.array([[np.cos(th), -np.sin(th), 0],
    #              [np.sin(th), np.cos(th),  0],
    #              [0, 0, 1]])
    R = np.array([[np.cos(th), 0, np.sin(th)],
                  [0,          1, 0],
                  [-np.sin(th), 0, np.cos(th)]])
    K = F.dot(R.dot(np.linalg.inv(F)))
    #R = np.array([[1.,0,0],
    #              [0,1.,0],
    #              [0,0,1.]])
    x_size = frame.shape[1] + 1000
    y_size = frame.shape[0] + 1000
    #newframe = cv2.undistort(frame, F, dist)
    paddedframe = cv2.copyMakeBorder(frame,500,500,500,500,cv2.BORDER_CONSTANT,value=[0,0,0])
    newframe = cv2.warpPerspective(paddedframe,K,(x_size,y_size))
    cv2.imshow(new_window,newframe[::4,::4,:])
    cv2.waitKey(30)