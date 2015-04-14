import cv2

fname = "c:\\Users\\Joseph\Videos\\2015-04-13 18-55-53\\Left.MP4"

# Open video for reading
cap = cv2.VideoCapture(fname)
if(not cap.isOpened()):
    print "Cannot open video file"
    print fname
    quit()

window_name = "Video"
cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, 13100)
print cap.get(cv2.cv.CV_CAP_PROP_FPS), cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)

cv2.namedWindow(window_name,cv2.WINDOW_AUTOSIZE)
while True:
    print cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES), cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)

    # Read frame
    retval,frame = cap.read()
    if(not retval):
        break
    cv2.imshow(window_name,frame[::2,::2,:])
    cv2.waitKey()