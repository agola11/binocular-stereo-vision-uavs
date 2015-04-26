from __future__ import print_function
import cv2
import numpy as np

ix,iy = -1,-1
# mouse callback function
def print_coords(event,x,y,flags,param):
	global frame_count
	global f
	if event == cv2.EVENT_LBUTTONDOWN:
		print (str(frame_count) + ' ' + str(cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC))+ ' ' + str((x, y)))
		print (str(frame_count) + ' ' + str(cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC))+ ' ' + str((x, y)), file=f)


vid = 'output.mp4'
log = 'super_ball_track.log'

cap = cv2.VideoCapture('videos/'+vid)
cv2.namedWindow('vid')
cv2.setMouseCallback('vid', print_coords)

cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, 4900) # first valid frame

f = open(log, 'w') # log file to write to
frame_count = 0

while(True):
	_, img = cap.read()
	frame_count += 1
	cv2.imshow('vid',img)
	k = cv2.waitKey()
	if k == 27:
		break

cap.release()
cv2.destroyAllWindows()