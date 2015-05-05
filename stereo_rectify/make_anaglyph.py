#!/usr/bin/python

import numpy as np
import cv2

def make_analgyph(left, right):
	"""
	expects BGR images
	"""
	(b1, g1, r1) = cv2.split(left)
	(b2, g2, r2) = cv2.split(right)
	new_r = (0.7*g1+0.3*b1).astype(np.uint8)
	return cv2.merge((b2, g2, new_r))


def test():
	l = cv2.imread('Rotated_left.jpg')
	r = cv2.imread('Rotated_right.jpg')

	print l.dtype

	ana = make_analgyph(l, r)

	#ana = cv2.cvtColor(ana, cv2.COLOR_RGB2BGR)

	cv2.imshow('ana', ana)
	cv2.waitKey()