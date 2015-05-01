import tracking_reader as tr
import log_reader as lr
import numpy as np
import cv2
import mpl_toolkits.mplot3d as m3d
import matplotlib.pyplot as plt

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
print F
left_reader = lr.LogReader(l_logname,l_first_data_time_ms)
right_reader = lr.LogReader(r_logname,r_first_data_time_ms)

track = tr.TrackingReader(track_fname,right_reader,track_data_log_offset,F,30,1,vid_fname=vid_fname)
track.seek_time(r_rect_start_time_ms - track_data_log_offset)


num_points = 100
times = np.linspace(254008.733, 268241.733, num_points)
d = np.linspace(20,40,num_points)
ax = m3d.Axes3D(plt.figure(1))
for i in range(num_points):
    observer_loc = right_reader.get_ekf_loc_1d(times[i])
    ax.scatter3D(*observer_loc)
    ball_loc = track.get_mean(times[i],d[i])
    ax.scatter(*ball_loc,c='r')

cov = track.get_cov(times[50],d[50],6)
ax.scatter(*cov,c='g')

ax.set_xlim3d(-35,10)
ax.set_ylim3d(-22.5,32.5)
ax.set_zlim3d(-45,0)
ax.set_xlabel("North")
ax.set_ylabel("East")
ax.set_zlabel("Down")
plt.show()
    
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