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
        print self.F
        print self.newF
        #self.newF[0,0] = self.newF[0,0]*.9
        #self.newF[1,1] = self.newF[1,1]*.9
        print self.newF
        
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
        
    def get_frame(self, target_yaw, target_pitch, target_loc = None, distance = 0):
        """
        returns the next frame in the video, rectified to face direction 
        target_yaw and pitched target_pitch degrees down. distance describes a distance
        to use for the planar image approximation when conducting translational stabilization
        """
        # Read the next frame
        retval,frame = self.cap.read()
        assert(retval)            
    
        undistorted_frame = self.undistort_frame(frame)
        
        now = self.cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
        current_yaw = self.log.get_ekf_yaw(now)
        current_loc = self.log.get_ekf_loc(now)
        if target_loc == None:
            target_loc = self.log.get_desired_loc(now)
       
        # For debugging
        #current_loc = target_loc
        #target_loc = np.array([[0.,0.,0.]])
        #current_loc = target_loc
        #target_loc = current_loc
        #current_yaw = 0
        #target_yaw = current_yaw
        #target_pitch = self.pitch
        target_yaw = (target_yaw - current_yaw)*.75 + current_yaw
        
        # Calculate R1: World frame to camera frame
        R_y1 = self.yaw_matrix(ned2image_yaw(current_yaw))
        R_p1 = self.pitch_matrix(self.pitch) 
        R1 = R_p1.dot(R_y1)
        
        # Calculate R2: World frame to desired frame
        R_y2 = self.yaw_matrix(ned2image_yaw(target_yaw))
        R_p2 = self.pitch_matrix(target_pitch)
        R2 = R_p2.dot(R_y2)
        
        # Translation Vectors
        T1 = ned2wun_loc(current_loc)
        T2 = ned2wun_loc(target_loc)
        
        # Get plane equation for translational corrections
        if distance == 0:
            K = self.horizontal_plane_vector()
        else:
            K = self.plane_vector(distance, ned2image_yaw(target_yaw))
        
        # Calculate full homography and transform frame
        H = self.get_homography(R1,R2,T1,T2,K)
        rotated_frame = cv2.warpPerspective(undistorted_frame,H,(self.w,self.h))
        return rotated_frame, frame
        
    def get_homography(self,R1,R2,T1,T2,K):
        """
        Calculate the homography matrix to transform from extrinsic position
        R1,T1 to R2,T2 using an updated method. K defines a planar position in 
        world coordinates
        """
        # Calculate Rotation Matrix P
        F = self.newF
        Finv = np.linalg.inv(self.newF)
        R1inv = np.linalg.inv(R1)
        P = F.dot(R2.dot(R1inv.dot(Finv)))
        
        c = (1-K.T.dot(T1))
        H = P - 1/c*F.dot(R2.T.dot(T1-T2)).dot((Finv.T.dot(R1.T.dot(K))).T)

        return H
        
    def get_homography_old(self,R1,R2,T1,T2,K):
        """
        Calculate the homography matrix to transform from extrinsic position
        R1,T1 to R2,T2 using an older method. K defines a planar position in 
        world coordinates
        """
        # Calculate Rotation Matrix P
        F = self.newF
        Finv = np.linalg.inv(self.newF)
        R1inv = np.linalg.inv(R1)
        P = F.dot(R2.dot(R1inv.dot(Finv)))
        
        #Translation thang
        T3 = self.newF.dot(R2.dot(R1inv.dot(T1))) - self.newF.dot(T2)
        
        # Calculate full homography
        K = self.plane_vector(distance, ned2image_yaw(target_yaw))
        KtilT = K.T.dot(R1inv.dot(Finv))
        c = 1-KtilT.dot(F.dot(T1))
        H = P-1/c*T3.dot(KtilT)
        
        return H
        
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
        Pitch frame down by th radians
        """        
        th_rad = np.deg2rad(th)
        R = np.array([[1,               0,               0],
                      [0,  np.cos(th_rad), np.sin(th_rad)],
                      [0, -np.sin(th_rad), np.cos(th_rad)]])
        return R
        
    def vertical_plane_vector(self, dist, target_loc, target_yaw):
        """
        Returns the defining vector for a vertical plane dist cm away from the 
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

    def horizontal_plane_vector(self):
        """
        Returns the defining vector for a ground plane dist cm away from the 
        drone in WUN coordinates
        """
        # Normal vector 
        n_wun = np.array([[0], 
                          [1], 
                          [0]])
        
        K = n_wun/.000001
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
    West-Up-North frame used by the camera rotations.
    """
    print ned_loc
    wun_loc = np.array([[-ned_loc[0,1]], 
                        [-ned_loc[0,2]], 
                        [ned_loc[0,0]]])
    #wun_loc = wun_loc*100 #Convert from m to cm
    return wun_loc