import cv2

fname = "./output.mp4"
frame_idx = 1

# Open video for reading
cap = cv2.VideoCapture(fname)
if(not cap.isOpened()):
    print "Cannot open video file"
    print fname
    quit()

window_name = "Video"
#cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, 13100)
print cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)/cap.get(cv2.cv.CV_CAP_PROP_FPS)*1000
print cap.get(cv2.cv.CV_CAP_PROP_FPS), cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)


cv2.namedWindow(window_name,cv2.WINDOW_AUTOSIZE)
while True:
    print cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES), cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)

    # Read frame
    retval,frame = cap.read()
    if(not retval):
        break
    cv2.imshow(window_name,frame[::2,::2,:])
    k = cv2.waitKey()
    if k == ord('s'):
        print 'saving'
        cv2.imwrite('../train/ball_s_' + str(frame_idx) + '.jpg', frame)
        frame_idx += 1