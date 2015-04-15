import cv2
import numpy as np
from time import sleep
import log_reader as lr
import mono_rectify as mr
import stereo_rectify as sr
import subprocess as sp

# Rotation-based image rectification for a single eye

# TODO For this module:
# Reapply barrel distortion afterward correction
# Correct yaw measurements for camera pitch

#Initial flight start frame - 5476
l_fname = "c:\\Users\\Joseph\Videos\\2015-04-13 18-55-53\\Left.MP4"
l_logname = "c:\\Users\\Joseph\Videos\\2015-04-13 18-55-53\\Left.log"
l_rect_start_frame = 14380
l_first_data_time_ms = 8408.4

stereo_offset = (8475.13333 - 8408.4)*30/1000

r_fname = "c:\\Users\\Joseph\Videos\\2015-04-13 18-55-53\\Right.MP4"
r_logname = "c:\\Users\\Joseph\Videos\\2015-04-13 18-55-53\\Right.log"
r_rect_start_frame = l_rect_start_frame + int(stereo_offset)
r_first_data_time_ms = 26092.73333
#8475.1333 = 254 frames

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
left_reader = lr.LogReader(l_logname,l_first_data_time_ms)
left_mono = mr.MonoRectify(l_fname, left_reader, F, dist)
left_mono.seek_frame(l_rect_start_frame)

right_reader = lr.LogReader(r_logname,r_first_data_time_ms)
right_mono = mr.MonoRectify(r_fname, right_reader, F, dist)
right_mono.seek_frame(r_rect_start_frame)

rectifier = sr.StereoRectify(left_mono,right_mono)

# Start VideoWriter
output_fname = "c:\\Users\\Joseph\Videos\\2015-04-13 18-55-53\\Stereo_raw.avi"
width = int(right_mono.cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
height = int(right_mono.cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
fps = int(right_mono.cap.get(cv2.cv.CV_CAP_PROP_FPS))

print height, width
#ffmpeg_command = ["C:\\ffmpeg\\bin\\ffmpeg.exe"
#                '-y'
#                '-f','rawvideo',
#                '-vcodec','rawvideo',
#                '-s', '1920x1080', # size of one frame
#                '-pix_fmt', 'rgb24',
#                '-r', '30', # frames per second
#                '-i', '-', # The imput comes from a pipe
#                '-an', # Tells FFMPEG not to expect any audio
#                '-vcodec', 'mpeg',
#                '\"c:\\Users\\Joseph\\Videos\\2015-04-13 18-55-53\\Stereo.MP4\"' ]
#pipe = sp.Popen(ffmpeg_command, shell=True, stdin = sp.PIPE, stderr = sp.PIPE)

#writer = cv2.VideoWriter(output_fname, cv2.cv.FOURCC(*'XVID'),fps,(height,width))
#writer = cv2.VideoWriter(output_fname, -1,fps,(width/2,height/2))
#if not writer.isOpened():
#    print "error opening output file"
#    quit()
    

for i in range(400):
    stitched_frame = rectifier.get_frame(245)
    print stitched_frame.shape
 #   writer.write(stitched_frame[::2,::2,:])
    #pipe.communicate( stitched_frame.tostring() )

    #cv2.imshow(orig_window,orig_frame[::2,::2,:])
    cv2.imshow(new_window,stitched_frame[::2,::2,:])
    cv2.waitKey(20)
#writer.release()