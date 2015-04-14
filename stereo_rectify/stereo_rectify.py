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
    
    def __init__(self, left, right):
        """
        Contructs a new StereoRectifiy object using MonoRectifies 
        left and right
        """
        self.left = left
        self.right = right
        
    def get_frame(self, target_th):
        """
        Returns a side-by-side stitching of the next left and right frames
        """
        left_frame, old_frame = self.left.get_frame(target_th)
        right_frame, old_frame = self.right.get_frame(target_th)
        
        #sanity check
        (h,w) = left_frame.shape[:2]
        assert((h,w) == right_frame.shape[:2])
        assert(h == OCULUS_HEIGHT)
        assert(w > OCULUS_WIDTH)
        
        #grab middle 960 pixels from both frames
        edge = (w-OCULUS_WIDTH)/2
        left_trim = left_frame[:,edge:OCULUS_WIDTH+edge]
        right_trim = right_frame[:,edge:OCULUS_WIDTH+edge]
        
        print left_trim.shape
        return np.append(left_trim,right_trim,axis=1)
        
    
