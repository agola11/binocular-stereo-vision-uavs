import numpy as np
from scipy import interpolate
#import matplotlib.pyplot as plt
import csv

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
        
        #plt.figure(1)
        #plt.plot(ekf_time,ekf_pd)
        
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
        
    def get_ekf_loc(self, t):
        """
        """
        loc = (self.ekf_pn_func(t), self.ekf_pe_func(t), self.ekf_pd_func(t))
        return loc
        