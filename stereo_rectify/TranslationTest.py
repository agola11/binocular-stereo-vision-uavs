import cv2
import numpy as np
from time import sleep
import log_reader as lr
import mono_rectify as mr

# Rotation-based image rectification for a single eye

# first_data_frame occurs 10 frames after the green light appears on the pixhawk
fname = "c:\\Users\\Joseph\Videos\\Planar Test\\Planar.MP4"
rect_start_time = 127761
first_data_time = 12345.66
num_frames = 1200

# first_data_frame occurs 10 frames after the green light appears on the pixhawk
#fname = "c:\\Users\\Joseph\Videos\\TranslationTest\\Trans.MP4"
#rect_start_time = 1.1101 #Frame 33
#rect_end_time = 37470.766 #1123
#first_data_time = 12345.66
#trans = np.linspace(0, -.75*0.787, num=1090)
#locs = np.zeros((1090,3))
#locs[:,1] = trans

#fname = "c:\\Users\\Joseph\Videos\\TranslationTest\\Forward.MP4"
#rect_start_time = 10343 #Frame 310
#rect_end_time = 37470.766 #1138
#first_data_time = 12345.66
#num_frames = 1138-310
#trans = np.linspace(0, -0.5588, num=num_frames)
#locs = np.zeros((num_frames,3))
#locs[:,0] = trans

#fname = "c:\\Users\\Joseph\Videos\\TranslationTest\\Down.MP4"
#rect_start_time = 24357.6 #Frame 730
#rect_end_time = 37470.766 #1345
#first_data_time = 12345.66
#num_frames = 1345-730
#trans = np.linspace(0, 0.5334, num=num_frames)
#locs = np.zeros((num_frames,3))
#locs[:,2] = trans


#fname = "c:\\Users\\Joseph\Videos\\Planar Test\\Rotation.MP4"
#rect_start_time = 0
#first_data_time = 0

F = np.array([[  1.65378644e+03,   0.00000000e+00,   9.35778810e+02],
              [  0.00000000e+00,   1.66564440e+03,   5.29772404e+02],
              [  0.00000000e+00,   0.00000000e+00,   1.00000000e+00]])
dist = np.array([[-0.48381301,  0.43026754, -0.00087523,  0.00879241, -0.31198885]] )

# Open windows for output
orig_window = "Original Video"
new_window = "Adjusted Video"
cv2.namedWindow(orig_window,cv2.WINDOW_AUTOSIZE)
cv2.namedWindow(new_window,cv2.WINDOW_AUTOSIZE)

# Start log reader and mono rectifier
reader = lr.LogReader("c:\\Users\\Joseph\\Videos\\Planar Test\\Planar.log",first_data_time)
mono = mr.MonoRectify(fname, reader, F, dist, 0)
mono.seek_time(rect_start_time)

for i in range(0,num_frames):
    #target_loc = locs[i,:]
    #print target_loc
    #target_loc = np.array([target_loc])
    #new_frame, orig_frame = mono.get_frame(0, 0, target_loc, 310)
    new_frame, orig_frame = mono.get_frame(160,0,518,np.array([[0.,0.,-2]])) 
    
    cv2.imshow(orig_window,orig_frame[::2,::2,:])
    cv2.imshow(new_window,new_frame[::2,::2,:])
    cv2.waitKey(20)
    