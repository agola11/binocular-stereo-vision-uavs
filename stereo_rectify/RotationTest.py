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

# first_data_frame occurs 10 frames after the green light appears on the pixhawk
fname = "c:\\Users\\Joseph\Videos\\2015-04-07 23-51-23 3.MP4"
rect_start_frame = 2240
first_data_frame = 310

F = np.array([[  1.50017800e+03,   0.00000000e+00,   9.45583379e+02],
              [  0.00000000e+00,   1.50991558e+03,   5.40817307e+02],
              [  0.00000000e+00,   0.00000000e+00,   1.00000000e+00]])
dist = np.array([[-0.47135957,  0.32651474, -0.00792725, -0.0019949,  -0.13798072]] )

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
    
    #Undistort frame
    h,  w = frame.shape[:2]
    newF, roi=cv2.getOptimalNewCameraMatrix(F,dist,(w,h),0)
    undistored_frame = cv2.undistort(frame, F, dist, newCameraMatrix = newF)
    x,y,w,h = roi
    undistored_frame = undistored_frame[y:y+h, x:x+w]
    
    # Find index for attitude data
    now = cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
    
    # Rotation!
    print cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
    th = np.deg2rad((reader.get_yaw(now-first_data_time_ms) - 287.72))
    #th = ((reader.get_yaw(now-first_data_time_ms) - 287.72)/70.)
    #th = 0
    #R = np.array([[1, 0, 0],
    #             [0, np.cos(th), -np.sin(th)],
    #             [0, np.sin(th), np.cos(th)]])
    #R = np.array([[np.cos(th), -np.sin(th), 0],
    #              [np.sin(th), np.cos(th),  0],
    #              [0, 0, 1]])
    R = np.array([[np.cos(th), 0, np.sin(th)],
                  [0,          1, 0],
                  [-np.sin(th), 0, np.cos(th)]])
    K = newF.dot(R.dot(np.linalg.inv(newF)))
    #R = np.array([[1.,0,0],
    #              [0,1.,0],
    #              [0,0,1.]])
    x_size = undistored_frame.shape[1] + 1000
    y_size = undistored_frame.shape[0] + 1000
    #paddedframe = cv2.copyMakeBorder(undistored_frame,500,500,500,500,cv2.BORDER_CONSTANT,value=[0,0,0])
    #newframe = cv2.warpPerspective(paddedframe,K,(x_size,y_size))
    newframe = cv2.warpPerspective(undistored_frame,K,(frame.shape[1],frame.shape[0]))
    cv2.imshow(new_window,newframe[::2,::2,:])
    cv2.waitKey(20)