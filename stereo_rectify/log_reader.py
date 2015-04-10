import numpy as np
from scipy import interpolate
import csv

'''
TODO:
Correct yaw measurements for camera pitch
'''

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
        
        self.time = np.array([])
        self.pitch = np.array([])
        self.yaw = np.array([])
        self.roll = np.array([])
        
        #Iterate over all messages in log file
        for row in reader:    
            if row[0] == 'ATT':
                self.time = np.append(self.time,float(row[1]))
                self.roll = np.append(self.roll,float(row[3]))
                self.pitch = np.append(self.pitch,float(row[5]))
                self.yaw = np.append(self.yaw,float(row[7]))
        attfile.close()
        
        # Instantiate interpolation functions
        self.yawfunc = interpolate.interp1d(self.time,self.yaw)
        self.pitchfunc = interpolate.interp1d(self.time,self.pitch)
        self.rollfunc = interpolate.interp1d(self.time,self.roll)
        
        #plt.figure(1)
       # plt.plot(self.time,self.yaw)
        #plt.show()
        
    def get_yaw(self,t):
        """
        Returns the yaw value at video time t, interpolated from the log file
        """
        return self.yawfunc(t - self.time_ref)