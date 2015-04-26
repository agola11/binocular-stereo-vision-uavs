import cv2
import numpy as np
from time import sleep
import log_reader as lr
import mono_rectify as mr
import stereo_rectify as sr
import subprocess as sp
#import matplotlib.pyplot as plt

# Rotation-based image rectification for a single eye

# TODO For this module:
# Reapply barrel distortion afterward correction
# Correct yaw measurements for camera pitch

#Initial flight start frame - 5476
l_fname = "c:\\Users\\Joseph\Videos\\Flight With Ball\\Left.MP4"
l_logname = "c:\\Users\\Joseph\Videos\\Flight With Ball\\Left.log"
l_rect_start_time_ms = 259000
l_first_data_time_ms = 14414.4

stereo_offset = (14481.133 - 14414.4)

r_fname = "c:\\Users\\Joseph\Videos\\Flight With Ball\\Right.MP4"
r_logname = "c:\\Users\\Joseph\Videos\\Flight With Ball\\Right.log"
r_rect_start_time_ms = l_rect_start_time_ms + int(stereo_offset)
r_first_data_time_ms = 31064.366
#8475.1333 = 254 frames

output_fname = "c:\\Users\\Joseph\Videos\\Flight With Ball\\Stereo.avi"
write_to_file = False
target_yaw = 250
target_pitch = -75
num_frames = 400

F = np.array([[  1.65378644e+03,   0.00000000e+00,   9.35778810e+02],
              [  0.00000000e+00,   1.66564440e+03,   5.29772404e+02],
              [  0.00000000e+00,   0.00000000e+00,   1.00000000e+00]])
dist = np.array([[-0.48381301,  0.43026754, -0.00087523,  0.00879241, -0.31198885]] )

# Open windows for output
orig_window = "Original Video"
new_window = "Adjusted Video"
cv2.namedWindow(orig_window,cv2.WINDOW_AUTOSIZE)
cv2.namedWindow(new_window,cv2.WINDOW_AUTOSIZE)

# Start log reader and mono rectifiers
left_reader = lr.LogReader(l_logname,l_first_data_time_ms)
left_reader.set_desired_loc_func(l_rect_start_time_ms, l_rect_start_time_ms + (num_frames+2)*1000/30)
left_mono = mr.MonoRectify(l_fname, left_reader, F, dist, -76)
left_mono.seek_time(l_rect_start_time_ms)

right_reader = lr.LogReader(r_logname,r_first_data_time_ms)
right_reader.set_desired_loc_func(r_rect_start_time_ms, r_rect_start_time_ms + (num_frames+2)*1000/30)
right_mono = mr.MonoRectify(r_fname, right_reader, F, dist, -74)
right_mono.seek_time(r_rect_start_time_ms)

#plt.figure(1)
#plt.show()
rectifier = sr.StereoRectify(left_mono,right_mono,yaw_offset = 0)

# Start VideoWriter
if(write_to_file):
    width = int(right_mono.cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
    height = int(right_mono.cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
    fps = int(right_mono.cap.get(cv2.cv.CV_CAP_PROP_FPS))
    writer = cv2.VideoWriter(output_fname, cv2.cv.FOURCC(*'XVID'),fps,(height,width))
    writer = cv2.VideoWriter(output_fname, -1,fps,(width/2,height/2))
    if not writer.isOpened():
        print "error opening output file"
        quit()
    

for i in range(num_frames):
    stitched_frame = rectifier.get_frame(target_yaw,target_pitch)
    print stitched_frame.shape

    if(write_to_file):
        writer.write(stitched_frame[::2,::2,:])
    
    #cv2.imshow(orig_window,orig_frame[::2,::2,:])
    cv2.imshow(new_window,stitched_frame[::2,::2,:])
    cv2.waitKey(20)

if(write_to_file):
    writer.release()