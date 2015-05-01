import cv2
import numpy as np
from time import sleep
import log_reader as lr
import mono_rectify as mr

# Rotation-based image rectification for a single eye

#fname = "c:\\Users\\Joseph\Videos\\FlightWithTelem.MP4"
#first_data_frame = 1712     # First frame with valid image data
#rect_start_frame = 4250     # Index of frame to start rectifying at

# first_data_frame occurs 10 frames after the green light appears on the pixhawk
fname = "c:\\Users\\Joseph\Videos\\2015-04-07 23-51-23 3.MP4"
rect_start_frame = 2240
first_data_frame = 310
first_data_time_ms = 10010.

F = np.array([[  1.50017800e+03,   0.00000000e+00,   9.45583379e+02],
              [  0.00000000e+00,   1.50991558e+03,   5.40817307e+02],
              [  0.00000000e+00,   0.00000000e+00,   1.00000000e+00]])
dist = np.array([[-0.47135957,  0.32651474, -0.00792725, -0.0019949,  -0.13798072]] )

# Open windows for output
orig_window = "Original Video"
new_window = "Adjusted Video"
cv2.namedWindow(orig_window,cv2.WINDOW_AUTOSIZE)
cv2.namedWindow(new_window,cv2.WINDOW_AUTOSIZE)

# Start log reader and mono rectifier
reader = lr.LogReader("2015-04-07 23-51-23 3.bin.log",first_data_time_ms)
mono = mr.MonoRectify(fname, reader, F, dist)
mono.seek_frame(rect_start_frame)

while(True):    
    new_frame, orig_frame = mono.get_frame(287.72)
    
    cv2.imshow(orig_window,orig_frame[::2,::2,:])
    cv2.imshow(new_window,new_frame[::2,::2,:])
    cv2.waitKey(20)