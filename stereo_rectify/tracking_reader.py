import numpy as np
import mpl_toolkits.mplot3d as m3d
import matplotlib.pyplot as plt
import cv2
from scipy import interpolate

# File type constants
class TrackingReader:
    
    """

    """
    
    def __init__(self, fname, log, data_start_time, F, baseline, trans_std, vid_fname=None):
        """
        """
        self.fname = fname
        self.log = log
        self.time_ref = data_start_time
        self.F = F
        
        if vid_fname != None:
            self.cap = cv2.VideoCapture(vid_fname)
            assert(self.cap.isOpened())
            self.w = int(self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
            self.h = int(self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
        
        # Read in camera log
        image_positions = self.read_camera_log()
        self.pixelx = interpolate.interp1d(self.time, image_positions[0,:])
        self.pixely = interpolate.interp1d(self.time, image_positions[1,:])
        n = image_positions.shape[1]
        
        # Get vectors towards ball in the right-handed camera frame
        vectors = self.get_ball_vector(image_positions)
        sigma_points = self.get_sigma_points(trans_std,
                                             trans_std,
                                             baseline,
                                             n)
                                             
        ax = m3d.Axes3D(plt.figure(1))
        for i in range(0,n):
            # Translate sigma_points into camera coords
            cam_center = vectors[:,i]*baseline
            cam_points = sigma_points[i,:,:] + cam_center[:,None]
            # Rotate into body coords
            body_center = self.camera2body(cam_center)
            body_points = self.camera2body(cam_points)
            # Rotate into vehicle frame
            R = self.get_R(self.time[i])
            Rinv = np.linalg.inv(R)
            ned_center = Rinv.dot(body_center)
            ned_points = Rinv.dot(body_points)
            # Translate into inertial frame
            T = self.get_T(self.time[i])
            world_center = ned_center + T
            world_points = ned_points + T[:,None]
            ax.scatter3D(*T)
            ax.scatter(*world_center,s = 1,c='r')
        plt.show()
    
    def get_mean(self, t, d):
        """
        Returns the location of the target in the NED world frame assuming distance
        d
        """
        im_pos = np.array([self.pixelx(t),self.pixely(t),1])
        vec = self.get_ball_vector(im_pos)
        cam_center = vec*d
        body_center = self.camera2body(cam_center)
        # Rotate into vehicle frame
        R = self.get_R(t)
        Rinv = np.linalg.inv(R)
        ned_center = Rinv.dot(body_center)
        # Translate into inertial frame
        T = self.get_T(t)
        inertial_center = ned_center + T
        return inertial_center
        
    def get_cov(self,t,d,sig_perp):
        """
        Returns the covariance estimate at time t approximating distance d
        """
        sig_x = np.array([sig_perp,0,0])
        sig_y = np.array([0,sig_perp,0])
        im_pos = np.array([self.pixelx(t),self.pixely(t),1])
        perp_points = np.vstack((im_pos-sig_x,
                                 im_pos + sig_x,
                                 im_pos - sig_y,
                                 im_pos + sig_y)).T
        
        # Calculate center and sigma points in camera frame
        vec = self.get_ball_vector(im_pos)
        cam_center = vec*d
        cam_sig = self.get_ball_vector(perp_points)*d
        cam_sig = np.vstack((cam_sig.T, vec*.1*d, vec*1.9*d)).T
        
        # Rotate into body frame
        body_center = self.camera2body(cam_center)
        body_sig = self.camera2body(cam_sig)
        
        # Rotate into vehicle frame
        R = self.get_R(t)
        Rinv = np.linalg.inv(R)
        ned_center = Rinv.dot(body_center)
        ned_sig = Rinv.dot(body_sig)
        
        # Translate into inertial frame
        T = self.get_T(t)
        inertial_center = ned_center + T
        inertial_sig = ned_sig + T[:,None]
        return inertial_sig
        
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
        
    def get_frame(self,target_yaw):
        """
        """
        # Read the next frame
        retval,frame = self.cap.read()
        assert(retval)
        
        t_adj = self.cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC) + self.time_ref
    
        cam2bod = np.array([[1, 0,  0],
                            [0, 0, -1],
                            [0, 1,  0]])
        bod2cam = np.linalg.inv(cam2bod)
        R1 = self.get_rotation_matrix(self.log.get_ekf_att(t_adj))
        R1inv = np.linalg.inv(R1)
        F = self.F
        Finv = np.linalg.inv(F)
        #target_att = self.log.get_ekf_att(t_adj)
        target_att = np.array([0,0,target_yaw])
        R2 = self.get_rotation_matrix(target_att)
        H = F.dot(bod2cam.dot(R2.dot(R1inv.dot(cam2bod.dot(Finv)))))
        rotated_frame = cv2.warpPerspective(frame,H,(self.w,self.h))
        return rotated_frame,frame
        
    def read_camera_log(self):
        """
        """
        # Read & parse attitude data
        attfile = open(self.fname,'r')
        
        time = np.array([])
        x = np.array([])
        y = np.array([])
        
        #Iterate over all messages in log file
        for line in attfile:
            words = line.split(" ")
            timestring = words[1]
            xstring = words[2][1:-1]
            ystring = words[3][0:-2]
            time = np.append(time, float(timestring))
            x = np.append(x,float(xstring))
            y = np.append(y,float(ystring))
        attfile.close()
        
        self.time = time + self.time_ref #Time is in right camera time
        imagepos = np.vstack((x,y,np.ones(y.shape[0])))
        return imagepos
        
    def get_ball_vector(self, imagepos):
        """
        """
        Finv = np.linalg.inv(self.F)
        rays = Finv.dot(imagepos)
        norms = np.linalg.norm(rays,axis=0)
        unit_rays = rays/norms
        return unit_rays
        
    def get_sigma_points(self,sig_x,sig_y,sig_z,num):
        """
        """
        point = np.array([[sig_x,-sig_x,    0,     0,    0,     0],
                          [    0,     0,sig_y,-sig_y,    0,     0],
                          [    0,     0,    0,     0,sig_z,-sig_z]])
        points = np.tile(point,(num,1,1))
        return points
    
    def get_R(self,t):
        """
        """
        att = self.log.get_ekf_att(t)
        R = self.get_rotation_matrix(att)
        return R
        
    def get_rotation_matrix(self, att):
        
        att = np.deg2rad(att)
        r_pitch = np.array([[ np.cos(att[1]), 0, -np.sin(att[1])],
                            [              0, 1,               0],
                            [ np.sin(att[1]), 0,  np.cos(att[1])]])
        r_roll = np.array([[1,               0,              0],
                           [0,  np.cos(att[0]), np.sin(att[0])],
                           [0, -np.sin(att[0]), np.cos(att[0])]])
        r_yaw = np.array([[  np.cos(att[2]), np.sin(att[2]), 0],
                          [ -np.sin(att[2]), np.cos(att[2]), 0],
                          [               0,              0, 1]])
        R = r_roll.dot(r_pitch.dot(r_yaw))
        return R
        
    def get_T(self,t):
        """
        """
        return self.log.get_ekf_loc_1d(t)
        
    def camera2body(self,p):
        """
        """
        R = np.array([[1, 0,  0],
                      [0, 0, -1],
                      [0, 1,  0]])
        return R.dot(p)