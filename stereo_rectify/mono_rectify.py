import numpy as np
import cv2

'''
TODO:
Implement rotations for when camera is pitched down
'''

class MonoRectify:
    """
    MonoRectify is a wrapper for cv2.capture that handles fisheye removal and 
    stabilization for a single GoPro video feed, one frame at a time
    """
    
    def __init__(self, fname, log, F, dist, pitch):
        """
        Creates a new MonoRectify object to read video from video file fname
        using attitude data from LogReader log, using camera matrix F and
        distortion coefficients dist. The camera is assumed to be pitched down
        by pitch degrees.
        """
        self.log = log
        self.F = F
        self.dist = dist
        self.fname = fname
        self.pitch = pitch
        
        # Open video for reading
        self.cap = cv2.VideoCapture(fname)
        assert(self.cap.isOpened())
        self.fps = self.cap.get(cv2.cv.CV_CAP_PROP_FPS)
        self.w = int(self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
        self.h = int(self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
        
        # Get new camera matrix for post-distortion removal transformations
        self.newF, self.roi=cv2.getOptimalNewCameraMatrix(self.F, self.dist,
                                                         (self.w,self.h),0)
    
    def seek_frame(self, frame):
        """
        sets the next frame to be rectified
        """
        self.cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frame)
        
    def get_frame(self, target_yaw, target_pitch, target_loc):
        """
        returns the next frame in the video, rectified to face direction 
        target_yaw and pitched target_pitch degrees down
        """
        # Read the next frame
        retval,frame = self.cap.read()
        assert(retval)            
    
        undistorted_frame = self.undistort_frame(frame)
        
        now = self.cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
        
        #Calculate R1: World frame to camera frame
        R_y1 = self.yaw_matrix(ned2image_yaw(self.log.get_ekf_yaw(now)))
        R_p1 = self.pitch_matrix(self.pitch) #TODO: Invert Pitch?
        R1 = R_p1.dot(R_y1)
        
        #Calculate R2: World frame to desired frame
        R_y2 = self.yaw_matrix(ned2image_yaw(target_yaw))
        R_p2 = self.pitch_matrix(target_pitch)
        R2 = R_p2.dot(R_y2)
        
        #Calculate Rotation Matrices
        newFinv = np.linalg.inv(self.newF)
        R1inv = np.linalg.inv(R1)        
        K = self.newF.dot(R2.dot(R1inv.dot(newFinv)))
        
        rotated_frame = cv2.warpPerspective(frame,K,(self.w,self.h))
        return rotated_frame, frame
        
    def undistort_frame(self, frame):
        """
        Removes fisheye distortion from frame
        """
        # Apply undistortion and crop
        undistorted_frame = cv2.undistort(frame, self.F, self.dist, 
                                          newCameraMatrix = self.newF)
        x,y,w,h = self.roi
        undistorted_frame = undistorted_frame[y:y+h+1, x:x+w+1]
        
        return undistorted_frame
        
    def yaw_matrix(self, th):
        """
        Rotates frame by th degrees
        """
        #R = np.array([[1, 0, 0],
        #             [0, np.cos(th), -np.sin(th)],
        #             [0, np.sin(th), np.cos(th)]])
        #R = np.array([[np.cos(th), -np.sin(th), 0],
        #              [np.sin(th), np.cos(th),  0],
        #              [0, 0, 1]])
        th_rad = np.deg2rad(th)
        R = np.array([[np.cos(th_rad),  0, np.sin(th_rad)],
                      [0,               1, 0],
                      [-np.sin(th_rad), 0, np.cos(th_rad)]])
        return R
        
    def pitch_matrix(self, th):
        """
        Pitch frame up by th radians
        """        
        th_rad = np.deg2rad(th)
        R = np.array([[1, 0,              0],
                      [0, np.cos(th_rad), -np.sin(th_rad)],
                      [0, np.sin(th_rad), np.cos(th_rad)]])
        return R

def ned2image_yaw(th):
    """
    Converts a yaw angle in the North-East-Down frame to the 
    yaw frame used by camera rotation matrices
    """
    return 360 - th