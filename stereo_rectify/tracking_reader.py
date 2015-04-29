import numpy as np

# File type constants
class TrackingReader:
    
    """

    """
    
    def __init__(self, fname, log, data_start_time, F, baseline, trans_std):
        """
        """
        self.fname = fname
        self.log = log
        self.time_ref = data_start_time
        self.F = F
        
        
        # Read in camera log
        image_positions = self.read_camera_log()
        n = image_positions.shape[1]
        
        # Get vectors towards ball in the right-handed camera frame
        vectors = self.get_ball_vectors(image_positions)
        sigma_points = self.get_sigma_points(trans_std,
                                             trans_std,
                                             baseline,
                                             n)
                                             
        for i in range(n):
            #Translate sigma_points into camera coords
            cam_center = vectors[:,i]*baseline
            cam_points = sigma_points[i,:,:] + cam_center[:,None]
            #Transform into body coords
            body_center = self.camera2body(cam_center)
            body_points = self.camera2body(cam_points)
            #Transform into NED coords
            R = self.get_R(i)
            ned_center = R.dot(body_center)
            ned_points = R.dot(body_center)
            print body_points
        
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
        
        time = time + self.time_ref #Time is in right camera time
        imagepos = np.vstack((x,y,np.ones(y.shape[0])))
        return imagepos
        
    def get_ball_vectors(self, imagepos):
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
    
    def get_R(self,i):
        """
        """
        att = self.log.get_ekf_att(self.time[i])
        att = np.deg2rad(att)
        r_pitch = np.array([[ np.cos(att[1]), 0, -np.sin(att[1])],
                            [              0, 1,               0],
                            [ np.sin(att[1]), 0,  np.cos(att[1])]])
        r_roll = np.array([[1,               0,              0],
                           [0,  np.cos(att[0]), np.sin(att[0])],
                           [0, -np.sin(att[0]), np.cos(att[0])]])
        r_yaw = np.array([[ np.cos(att[2]), np.sin(att[2]), 0],
                          [ -np.sin(att[2]), np.cos(att[2]), 0],
                          [              0,              0, 1]])
        R = r_roll.dot(r_pitch.dot(r_yaw))
        return R
        
    def camera2body(self,p):
        """
        """
        R = np.array([[1, 0,  0],
                      [0, 0, -1],
                      [0, 1,  0]])
        return R.dot(p)