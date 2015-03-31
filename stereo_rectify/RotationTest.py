import cv2
import numpy as np
from time import sleep
from scipy import interpolate

# Rotation-based image rectification for a single eye

fname = "c:\\Users\\Joseph\Videos\\FlightWithTelem.MP4"
first_data_frame = 1712     # First frame with valid image data
rect_start_frame = 4250     # Index of frame to start rectifying at

F = np.array([[1.21710707e+03,   0.00000000e+00,   1.36923928e+03],
              [0.00000000e+00,   1.22282317e+03,   9.78605574e+02],
              [0.00000000e+00,   0.00000000e+00,   1.00000000e+00]])
dist = np.array([[ -3.19826380e-01,   1.74633694e-01,   2.05930039e-04,   2.01208997e-04, -8.69545436e-02]] )

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

# Read & parse attitude data
attfile = open('attitude.log','r')
i = 0
time = np.array([])
pitch = np.array([])
yaw = np.array([])
roll = np.array([])
for line in attfile:
    words = line.split("=")
    timestring = words[0].split(":")[0]
    pitchstring = words[1].split(",")[0]
    yawstring = words[2].split(",")[0]
    rollstring = words[3].split(",")[0]
    
    if i == 0:
        time = np.append(time,float(timestring))
        pitch = np.append(pitch,float(pitchstring))
        yaw = np.append(yaw,float(yawstring))
        roll = np.append(roll,float(rollstring))
        i = i + 1
    elif (float(pitchstring) != pitch[i-1] or
            float(yawstring) != yaw[i-1] or
           float(rollstring) != roll[i-1]):
        time = np.append(time,float(timestring))
        pitch = np.append(pitch,float(pitchstring))
        yaw = np.append(yaw,float(yawstring))
        roll = np.append(roll,float(rollstring))
        i = i + 1
print yaw.shape, time.shape, time[-1]

# Interpolate yaw values for each frame
yawfunc = interpolate.interp1d(time,yaw)
time = np.linspace(time[0],time[-1],(time[-1]-time[0])*fps)
yaw = yawfunc(time)
print yaw, yaw.shape, time.shape, time[-1]

while(True):
    # Find index for attitude data
    now = cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
    index = (np.abs(time*1000 + first_data_time_ms - now)).argmin()
    print index
    print now, first_data_time_ms,time[-1]*1000 + first_data_time_ms
    
    # Read frame
    retval,frame = cap.read()
    if(not retval):
        break
    cv2.imshow(orig_window,frame[::2,::2,:])
    
    # Rotation!
    th = 2.45 - yaw[index]
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