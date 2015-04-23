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
        
    def seek_time(self, time):
        """
        sets the time from which to select the next frame to be rectified in ms
        """
        self.cap.set(cv2.cv.CV_CAP_PROP_POS_MSEC, time)
        
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
        current_yaw = self.log.get_ekf_yaw(now)
        current_loc = self.log.get_ekf_loc(now)
        target_loc = self.log.get_desired_loc(now)
        
        # For debugging
        target_loc = current_loc
        #target_yaw = current_yaw
        #target_pitch = self.pitch
        
        # Calculate R1: World frame to camera frame
        R_y1 = self.yaw_matrix(ned2image_yaw(current_yaw))
        R_p1 = self.pitch_matrix(self.pitch) 
        R1 = R_p1.dot(R_y1)
        
        # Calculate R2: World frame to desired frame
        R_y2 = self.yaw_matrix(ned2image_yaw(target_yaw))
        R_p2 = self.pitch_matrix(target_pitch)
        R2 = R_p2.dot(R_y2)
        
        # Calculate Rotation Matrix P
        newFinv = np.linalg.inv(self.newF)
        R1inv = np.linalg.inv(R1)
        P = self.newF.dot(R2.dot(R1inv.dot(newFinv)))
       
        # Translation Vectors
        T1 = ned2wun_loc(current_loc)
        T2 = ned2wun_loc(target_loc)
        T3 = -self.newF.dot(R2.dot(R1inv.dot(T1))) + self.newF.dot(T2)
        print self.newF.dot(R2.dot(R1inv.dot(T1))), self.newF.dot(T2)
        
        # Calculate full homography
        K = self.plane_vector(10000, ned2image_yaw(target_yaw))
        KtilT = K.T.dot(R1inv.dot(newFinv))
        print KtilT
        print P
        c = 1-KtilT.dot(self.newF.dot(T1))
        print T3.dot(KtilT)
        H = P-1/c*T3.dot(KtilT)
        rotated_frame = cv2.warpPerspective(undistorted_frame,H,(self.w,self.h))
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
        R = np.array([[ np.cos(th_rad), 0, np.sin(th_rad)],
                      [              0, 1,              0],
                      [-np.sin(th_rad), 0, np.cos(th_rad)]])
        return R
        
    def pitch_matrix(self, th):
        """
        Pitch frame up by th radians
        """        
        th_rad = np.deg2rad(th)
        R = np.array([[1,              0,               0],
                      [0, np.cos(th_rad), -np.sin(th_rad)],
                      [0, np.sin(th_rad),  np.cos(th_rad)]])
        return R
        
    def plane_vector(self, dist, target_yaw):
        """
        Returns the defining vector for a plane dist cm away from the 
        camera in WUN coordinates
        """
        th_rad = np.deg2rad(target_yaw)
        # Normal vector 
        # TODO: Check this for all yaw quadrants
        n_wun = np.array([[np.sin(th_rad)], 
                          [0], 
                          [np.cos(th_rad)]])
        
        K = n_wun/dist
        return K

def ned2image_yaw(th):
    """
    Converts a yaw angle in the North-East-Down frame to the 
    yaw frame used by camera rotation matrices
    """
    return 360 - th
    
def ned2wun_loc(ned_loc):
    """
    Converts a location in the North-East-Down coordinate frame to the 
    West-Up-North frame used by the camera rotations. Converts from m to
    cm in doing so.
    """
    print ned_loc
    wun_loc = np.array([[-ned_loc[0,1]], 
                        [-ned_loc[0,2]], 
                        [ned_loc[0,0]]])
    wun_loc = wun_loc*100
    return wun_loc