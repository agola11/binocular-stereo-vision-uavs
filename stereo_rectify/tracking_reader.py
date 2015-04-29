import numpy as np

# File type constants
class TrackingReader:
    
    """

    """
    
    def __init__(self, fname, log, data_start_time, F):
        """
        """
        self.fname = fname
        self.log = log
        self.time_ref = data_start_time
        self.F = F
        
        # Read in camera log
        self.read_camera_log()
    
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
            ystring = words[3][0,-1]
            time = np.append(time, float(timestring))
            x = np.append(x,float(xstring)
            y = np.append(y,float(ystring)
        attfile.close()
        
        time = time - self.time_ref
        
        