import cv2
import time

cap = cv2.VideoCapture(-1)
class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
    def __enter__(self):
        self.start = time.time()
        return self
    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            print 'elapsed time: %f ms' % self.msecs

for i in range(0,4):
    start = time.time()
    for j in range(0,10):
        _, frame = cap.read()
    end = time.time()
    elapsed = end-start
    fps = 10/elapsed
    print "10 frames: {e} seconds, {f} fps".format(e=elapsed,f=fps)
cap.release()
