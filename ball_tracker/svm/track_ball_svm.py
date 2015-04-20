'''
track_ball_svm.py:
	Track ball using previously trained 2-class SVM.
	Create an output video and log.
Author:
	Ankush Gola
'''

from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.externals import joblib
import time
import cv2

def flatten(img):
	"""
	Flatten a color image into a vector of pixels
	"""
	M, N, P = img.shape
	return img.reshape(M*N, P)

vw = cv2.VideoWriter

frame_count = 1
<<<<<<< HEAD
vid = 'sunny_test.mov'
out = 'out.avi'
=======
vid = 'cloudy_test.mov'
out = 'out_cloudy.avi'
>>>>>>> a82174cb19f7edee4d5f11406d7ca860ba907d87
log = 'ball_track.log'

clf2 = joblib.load('model/clf.pkl')  # read in the model
f = open(log, 'w') # log file to write to

cap = cv2.VideoCapture('videos/' + vid)

w, h = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.cv.CV_CAP_PROP_FPS))

vw = cv2.VideoWriter(out, cv2.cv.FOURCC(*'XVID'), fps, (w, h))
vw = cv2.VideoWriter(out, -1, fps, (w, h)) # initialize videowriter

while True:
	_, frame = cap.read()
	if (frame == None):
		break

	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	rgb_f = rgb.astype(float)/255 # scale for classification
	
	M, N, P = rgb_f.shape
	rgb_ff = flatten(rgb_f)

	Z = clf2.predict(rgb_ff)
	Z = Z.reshape(M, N)

	Z = cv2.GaussianBlur(Z.astype(np.float),(15,15),0)
	Z = (Z*255).astype(np.uint8)

	circles = cv2.HoughCircles(Z,cv2.cv.CV_HOUGH_GRADIENT,1,1600, param1 = 50, param2 = 10)
	if circles != None:
		(x, y, r) = circles[0,:][0]
		print (x, y, r)
		print (str(frame_count) + ' ' + str((x, y, r)), file=f)
		cv2.circle(frame, (x, y), r, (0,255,0), 2)
		cv2.circle(frame,(x, y), 3 ,(0,0,255),3)

	frame_count+=1

	vw.write(frame)
	cv2.imshow('frame',frame)
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

cap.release()
vw.release()
cv2.destroyAllWindows()