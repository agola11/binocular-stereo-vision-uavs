import cv2
import numpy as np

ix,iy = -1,-1
# mouse callback function
def print_coords(event,x,y,flags,param):
    global ix,iy
    ix,iy = x,y
    print ix, iy

cap = cv2.VideoCapture(0)
# Create a black image, a window and bind the function to window
cv2.namedWindow('image')
cv2.setMouseCallback('image', print_coords)

while(1):
	_, img = cap.read()
	cv2.imshow('image',img)
	k = cv2.waitKey(20) & 0xFF
	if k == 27:
		break

cap.release()
cv2.destroyAllWindows()