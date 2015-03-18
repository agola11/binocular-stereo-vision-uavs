'''
ball_tracker.py
Author:
	Ankush Gola, Joseph Bolling
'''

import cv2
import numpy as np
from iir_filter import IIRFilter

class BallTracker:
	"""
	BallTracker is a class that implements ball detection via hsv masking, dilation/erosion, and hough transform
	"""

	def __init__(self, cap=0, morph_close=21, morph_open=11, gauss=9, filter_tap=0):
		"""
		return an instance of BallTracker
		cap: which video capture to use
		morph_close: size of morphological close mask
		morph_open: size of morphological open mask
		gauss: size of gaussian blur mask
		filter_tap: weight in iir filter
		"""
		self.cap = cv2.VideoCapture(cap)
		self.h_lo, self.s_lo, self.v_lo = 0, 0, 0
		self.h_hi, self.s_hi, self.v_hi = 100, 100, 100
		self.hsv_lower = np.array([self.h_lo, self.s_lo, self.v_lo])
		self.hsv_upper = np.array([self.h_hi, self.s_hi, self.v_hi])
		self.kernel_close = np.ones((morph_close, morph_close),np.uint8)
		self.kernel_open = np.ones((morph_open, morph_open),np.uint8)
		self.gauss = gauss
		self.iir = None # will update this in detect_ball
		self.filter_tap = filter_tap

	def get_hsv_lo(self):
		"""
		return hsv lower bounds as np array
		"""
		return self.hsv_lower

	def get_hsv_hi(self):
		"""
		return hsv upper bounds as np array
		"""
		return self.hsv_upper

	def set_hsv_hi(self, (h, s, v)):
		"""
		set the hsv upper bounds as h, s, v
		"""
		self.h_hi, self.s_hi, self.v_hi = h, s, v
		self.hsv_upper = np.array([self.h_hi, self.s_hi, self.v_hi])

	def get_hsv_lo(self):
		"""
		return hsv upper bounds as np array
		"""
		return self.hsv_lower

	def set_hsv_lo(self, (h, s, v)):
		"""
		set the hsv upper bounds as h, s, v
		"""
		self.h_lo, self.s_lo, self.v_lo = h, s, v
		self.hsv_lower = np.array([self.h_lo, self.s_lo, self.v_lo])

	def release_cap(self):
		"""
		release the cap
		"""
		self.cap.release()

	def detect_ball(self, show_res=False, strat='HOUGH', morph=True, blur=True):
		"""
		detect the ball in the current frame and return the x, y radius of ball
		show_res: also return the resulting image with the detected circle drawn
		strat: which detector to use (TODO)
		morph: perform morphological operations
		blur: apply a blur to the mask before circle detection (usually helpful)
		"""
		_, frame = self.cap.read() # read a frame
		hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) # convert to HSV space
		mask = cv2.inRange(hsv, self.hsv_lower, self.hsv_upper)

		if morph:
			# do dilation and erosion
			mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.kernel_close)
			mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel_open)

		if blur:
			mask = cv2.GaussianBlur(mask,(self.gauss,self.gauss),0)

		circles = cv2.HoughCircles(mask,cv2.cv.CV_HOUGH_GRADIENT,1,1600, param1 = 50, param2 = 22)

		if circles != None:
			(x, y, r) = circles[0,:][0]

			# run the results through iir filter
			if self.iir == None:
				# create new IIRFilter if first run
				self.iir = IIRFilter(np.float32((x, y, r)), self.filter_tap)
			else:
				self.iir.update(np.float32((x, y, r)))

			[x, y, r] = self.iir.state()

			if show_res:
				result = cv2.bitwise_and(frame,frame,mask = mask)
				cv2.circle(result, (x, y), r, (0,255,0), 2)
				cv2.circle(result,(x, y), 3 ,(0,0,255),3)
				res = cv2.resize(result,None,fx=0.5, fy=0.5)
			else:
				res = None

			return (x, y, r, res)

		else:
			return None

"""
Testing
"""

def test():
	bt = BallTracker(filter_tap=0.5)
	bt.set_hsv_hi((178, 255, 255))
	bt.set_hsv_lo((127,98, 118))
	while True:
		state = bt.detect_ball(show_res=True)
		if state != None:
			(x, y, r, res) = state
			cv2.imshow('result',res)
			print (x, y, r)

		k = cv2.waitKey(5) & 0xFF
		if k == 27:
			break

	bt.release_cap()

test()








