import cv2

cap = cv2.VideoCapture(-1)

while True:
    _, frame = cap.read()
    print "got an image"
