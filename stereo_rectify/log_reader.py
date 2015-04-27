import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import csv
import mpl_toolkits.mplot3d as m3d

# File type constants
ATTITUDE_LOG_T = 1
FLASH_LOG_T = 2

class LogReader:
    
    """
    LogReader is a class for reading arducopter log files. It handles both 
    file input and interpolation to the desired time points. 
    
    LogReader is equipped to handle two types of log files - attitude log files,
    which contain only data about a drone's attitude, and flashdata log files, 
    which contain high frequency data about a variety of drone parameters.
    
    data_start_time is the timestamp in a video of the first time the pixhawk light
    turns on
    """
    
    def __init__(self, fname, data_start_time, ftype = FLASH_LOG_T):
        """
        Initialize a new LogReader object to collect data from file fname 
        of type ftype
        """
        self.fname = fname
        self.ftype = ftype
        self.time_ref = data_start_time + 343.67
        
        if ftype == ATTITUDE_LOG_T:
            self.read_attitude_log()
        elif ftype == FLASH_LOG_T:
            self.read_flash_log()
    
    def read_attitude_log(self):
        """
        Read data from the attitude log with name self.fname
        """
        # Read & parse attitude data
        attfile = open(self.fname,'r')
        i = 0
        self.time = np.array([])
        self.pitch = np.array([])
        self.yaw = np.array([])
        self.roll = np.array([])
        
        for line in attfile:
            words = line.split("=")
            timestring = words[0].split(":")[0]
            pitchstring = words[1].split(",")[0]
            yawstring = words[2].split(",")[0]
            rollstring = words[3].split(",")[0]
            
            if i == 0:
                self.time = np.append(self.time,float(timestring)*1000)
                self.pitch = np.append(self.pitch,float(pitchstring))
                self.yaw = np.append(self.yaw,float(yawstring))
                self.roll = np.append(self.roll,float(rollstring))
                i = i + 1
            elif (float(pitchstring) != self.pitch[i-1] or
                    float(yawstring) != self.yaw[i-1] or
                   float(rollstring) != self.roll[i-1]):
                self.time = np.append(self.time,float(timestring)*1000)
                self.pitch = np.append(self.pitch,float(pitchstring))
                self.yaw = np.append(self.yaw,float(yawstring))
                self.roll = np.append(self.roll,float(rollstring))
                i = i + 1
        attfile.close()
        
        # Instantiate interpolation functions
        self.yawfunc = interpolate.interp1d(self.time,self.yaw)
        self.pitchfunc = interpolate.interp1d(self.time,self.pitch)
        self.rollfunc = interpolate.interp1d(self.time,self.roll)

    def read_flash_log(self):
        """
        Read data from the vehicle flash log with name self.fname
        """
        attfile = open(self.fname,'r')
        reader = csv.reader(attfile)
        
        att_time = np.array([])
        att_pitch = np.array([])
        att_yaw = np.array([])
        att_roll = np.array([])
        
        ekf_time = np.array([])
        ekf_roll = np.array([])
        ekf_pitch = np.array([])
        ekf_yaw = np.array([])
        ekf_vn = np.array([])
        ekf_ve = np.array([])
        ekf_vd = np.array([])
        ekf_pn = np.array([])
        ekf_pe = np.array([])
        ekf_pd = np.array([])
        
        m_time = np.array([])
        m0 = np.array([])
        m1 = np.array([])
        m2 = np.array([])
        m3 = np.array([])
        m4 = np.array([])
        m5 = np.array([])
        m6 = np.array([])
        m7 = np.array([])
        
        #Iterate over all messages in log file
        for row in reader:    
            if row[0] == 'ATT':
                # Parse Attitude Data
                att_time = np.append(att_time,float(row[1]))
                att_roll = np.append(att_roll,float(row[3]))
                att_pitch = np.append(att_pitch,float(row[5]))
                att_yaw = np.append(att_yaw,float(row[7]))
            
            if row[0] == 'EKF1':
                # Parse EKF data
                ekf_time = np.append(ekf_time,float(row[1]))
                ekf_roll = np.append(ekf_roll,float(row[2]))
                ekf_pitch = np.append(ekf_pitch,float(row[3]))
                ekf_yaw = np.append(ekf_yaw,float(row[4]))
                ekf_vn = np.append(ekf_vn,float(row[5]))
                ekf_ve = np.append(ekf_ve,float(row[6]))
                ekf_vd = np.append(ekf_vd,float(row[7]))
                ekf_pn = np.append(ekf_pn,float(row[8]))
                ekf_pe = np.append(ekf_pe,float(row[9]))
                ekf_pd = np.append(ekf_pd,float(row[10]))
            if row[0] == 'RCOU':
                m_time = np.append(m_time,float(row[1]))
                m0 = np.append(m0,float(row[2]))
                m1 = np.append(m1,float(row[3]))
                m2 = np.append(m2,float(row[4]))
                m3 = np.append(m3,float(row[5]))
                m4 = np.append(m4,float(row[6]))
                m5 = np.append(m5,float(row[7]))
                m6 = np.append(m6,float(row[8]))
                m7 = np.append(m7,float(row[9]))
        attfile.close()
        
        # Instantiate interpolation functions
        self.yaw_func = interpolate.interp1d(att_time,att_yaw)
        self.pitch_func = interpolate.interp1d(att_time,att_pitch)
        self.roll_func = interpolate.interp1d(att_time,att_roll)
        
        self.ekf_roll_func = interpolate.interp1d(ekf_time, ekf_roll)
        self.ekf_pitch_func = interpolate.interp1d(ekf_time, ekf_pitch)
        self.ekf_yaw_func = interpolate.interp1d(ekf_time, ekf_yaw)
        self.ekf_vn_func = interpolate.interp1d(ekf_time, ekf_vn)
        self.ekf_ve_func = interpolate.interp1d(ekf_time, ekf_ve)
        self.ekf_vd_func = interpolate.interp1d(ekf_time, ekf_vd)
        self.ekf_pn_func = interpolate.interp1d(ekf_time, ekf_pn)
        self.ekf_pe_func = interpolate.interp1d(ekf_time, ekf_pe)
        self.ekf_pd_func = interpolate.interp1d(ekf_time, ekf_pd)
        
        self.m0_func = interpolate.interp1d(m_time, m0)
        self.m1_func = interpolate.interp1d(m_time, m1)
        self.m2_func = interpolate.interp1d(m_time, m2)
        self.m3_func = interpolate.interp1d(m_time, m3)
        self.m4_func = interpolate.interp1d(m_time, m4)
        self.m5_func = interpolate.interp1d(m_time, m5)
        self.m6_func = interpolate.interp1d(m_time, m6)
        self.m7_func = interpolate.interp1d(m_time, m7)
        
        print m_time[0], m_time[-1]
        
        positions = np.array([ekf_pn, -ekf_pe, -ekf_pd])
        ax = m3d.Axes3D(plt.figure(1))
        ax.scatter3D(*positions)
        
        ax.scatter3D(*positions)
        ax.set_xlim3d(-5,5)
        ax.set_ylim3d(-5,5)
        ax.set_zlim3d(-5,5)
        plt.show()
    
    def get_motor_vals(self,t):
        """
        returns an 8-vector containing the 8 motor outputs from the X8
        """
        t_adj = t-self.time_ref
        v = np.array([self.m0_func(t_adj),
                      self.m1_func(t_adj),
                      self.m2_func(t_adj),
                      self.m3_func(t_adj),
                      self.m4_func(t_adj),
                      self.m5_func(t_adj),
                      self.m6_func(t_adj),
                      self.m7_func(t_adj)])
        return v
    
    def get_ekf_vel(self,t):
        """
        returns the velocity of the drone in NED coordinates
        """
        t_adj = t-self.time_ref
        vel = np.array([self.ekf_vn_func(t_adj),
                        self.ekf_ve_func(t_adj),
                        self.ekf_vd_func(t_adj)])
        return vel
    
    def get_att_yaw(self,t):
        """
        Returns the yaw value at video time t, interpolated from the log file
        """
        return self.yaw_func(t - self.time_ref)
        
    def get_ekf_yaw(self,t):
        """
        Returns the yaw value as determined by the copter's onboard EKF at time t,
        interpolated from the log file
        """
        return self.ekf_yaw_func(t-self.time_ref)
        
    def get_ekf_att(self,t):
        """
        returns a 3-vector containing the (roll, pitch, yaw) of the UAV at time t
        """
        t_adj = t-self.time_ref
        att = np.array([self.ekf_roll_func(t_adj),
                        self.ekf_pitch_func(t_adj),
                        self.ekf_yaw_func(t_adj)])
        
        return att
        
    def get_ekf_loc(self, t):
        """
        Returns the NED location in meters relative to the drone's position when 
        armed
        """
        t_adj = t - self.time_ref
        loc = np.array([[self.ekf_pn_func(t_adj), 
                         self.ekf_pe_func(t_adj), 
                         self.ekf_pd_func(t_adj)]])
        return loc
        
    def get_ekf_loc_1d(self, t):
        """
        Returns the NED location in meters relative to the drone's position when 
        armed as a 1-dimensional numpy vector
        """
        t_adj = t - self.time_ref
        loc = np.array([self.ekf_pn_func(t_adj), 
                        self.ekf_pe_func(t_adj), 
                        self.ekf_pd_func(t_adj)])
        return loc
    
    
    def set_desired_loc_func(self, start_t, end_t):
        """
        Computes and saves a function describing the desired location between
        times start_t and end_t (in ms) using least-squares methods on the locations
        observed between those two times
        
        TODO: Rewrite to accept a desired starting and end altitude
              Consider accepting start/end positions orthogonal to the baseline
              might produce inverted path if copter starts west and moves east
        """
        # Collect position data for the times in question
        positions = self.get_ekf_loc(end_t)
        for t in np.arange(start_t, end_t, 1000./30):
            positions = np.append(positions, self.get_ekf_loc(t), axis=0)
            
        # Run svd to find the direction of maximum variation in the data
        mean = np.mean(positions,axis = 0)
        u,s,v = np.linalg.svd(positions-mean)
        dir = v[0]
        
        # Create points for desired location line
        end_pos_norm = -np.linalg.norm(self.get_ekf_loc(end_t) - mean)
        start_pos_norm = np.linalg.norm(self.get_ekf_loc(start_t) - mean)
        magnitudes = np.linspace(start_pos_norm,end_pos_norm)
        points = np.outer(dir, magnitudes.T) + np.outer(mean, np.ones(magnitudes.shape))
        
        # Create corresponding timestamps and interpolation functions
        t = np.linspace(start_t, end_t, num=magnitudes.shape[0]) - self.time_ref
        self.desired_pn_func = interpolate.interp1d(t, points[0,:])
        self.desired_pe_func = interpolate.interp1d(t, points[1,:])
        self.desired_pd_func = interpolate.interp1d(t, points[2,:])
        
        ax = m3d.Axes3D(plt.figure(1))
        ax.scatter3D(*positions.T)
        ax.plot3D(*points)
        ax.scatter3D(*self.get_ekf_loc(start_t).T, c='r')
        ax.scatter3D(*points[:,1],c='r')
        plt.show()
        
    def get_desired_loc(self,t):
        """
        returns the desired position at time t in NED coordinates. 
        set_desired_loc_func must be called before calling this function
        """
        t_adj = t - self.time_ref
        loc = np.array([[self.desired_pn_func(t_adj), 
                         self.desired_pe_func(t_adj), 
                         self.desired_pd_func(t_adj)]])
        return loc
        