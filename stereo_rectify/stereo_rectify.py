import numpy as np
import scipy as sp

'''
TODO:
fill this in... lol
separate method for two frames and two videos maybe?
'''

#Size of an eye display on the Oculus Rift, in pixels
OCULUS_WIDTH = 960
OCULUS_HEIGHT = 1080

class StereoRectify:
    
    def __init__(self, left, right, yaw_offset = 0):
        """
        Contructs a new StereoRectifiy object using MonoRectifies 
        left and right. th_offset provides a "toe out" amount by which to
        adjust the right image feed. 
        """
        self.left = left
        self.right = right
        self.yaw_offset = yaw_offset
        
    def get_frame(self, target_yaw, target_pitch):
        """
        Returns a side-by-side stitching of the next left and right frames
        """
        left_frame, old_frame = self.left.get_frame(target_yaw - self.yaw_offset/2, target_pitch,None)
        right_frame, old_frame = self.right.get_frame(target_yaw + self.yaw_offset/2, target_pitch,None)
        
        #sanity check
        (h,w) = left_frame.shape[:2]
        print h,w
        assert((h,w) == right_frame.shape[:2])
        assert(h == OCULUS_HEIGHT)
        assert(w > OCULUS_WIDTH)
        
        #grab middle 960 pixels from both frames
        edge = (w-OCULUS_WIDTH)/2
        left_trim = left_frame[:,edge:OCULUS_WIDTH+edge]
        right_trim = right_frame[:,edge:OCULUS_WIDTH+edge]
        
        print left_trim.shape
        return np.append(left_trim,right_trim,axis=1)
        
    
