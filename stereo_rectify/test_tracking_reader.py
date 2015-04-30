import tracking_reader as tr
import log_reader as lr
import numpy as np
import cv2

vid_fname = "c:\\Users\\Joseph\\Documents\\14-15\\Thesis\\SeniorThesis2015\\ball_tracker\\svm\\videos\\output.mp4"

l_fname = "c:\\Users\\Joseph\Videos\\Flight With Ball\\Left.MP4"
l_logname = "c:\\Users\\Joseph\Videos\\Flight With Ball\\Left.log"
l_rect_start_time_ms = 259000
l_first_data_time_ms = 14414.4

stereo_offset = (14481.133 - 14414.4)

r_fname = "c:\\Users\\Joseph\Videos\\Flight With Ball\\Right.MP4"
r_logname = "c:\\Users\\Joseph\Videos\\Flight With Ball\\Right.log"
r_rect_start_time_ms = l_rect_start_time_ms + int(stereo_offset)
r_first_data_time_ms = 31064.366

C920_data = np.load("C920_calib_data.npz")
F = C920_data['intrinsic_matrix']
track_fname = "super_ball_track.log"
track_offset = 30230   #tracking log is ~29998 ms behind left gopro
track_data_log_offset = track_offset + stereo_offset

left_reader = lr.LogReader(l_logname,l_first_data_time_ms)
right_reader = lr.LogReader(r_logname,r_first_data_time_ms)

track = tr.TrackingReader(track_fname,right_reader,track_data_log_offset,F,30,1,vid_fname=vid_fname)
track.seek_time(r_rect_start_time_ms - track_data_log_offset)
"""
orig_window = "Original Video"
new_window = "Adjusted Video"
cv2.namedWindow(orig_window,cv2.WINDOW_AUTOSIZE)
cv2.namedWindow(new_window,cv2.WINDOW_AUTOSIZE)

for i in range(300):
    rotated_frame, orig_frame = track.get_frame(253)
    
    cv2.imshow(orig_window,orig_frame[::2,::2,:])
    cv2.imshow(new_window,rotated_frame[::2,::2,:])
    cv2.waitKey(30)
"""