'''
diag_line.py
Author:
	Ankush Gola

Make the drone start from a given (lat, lon, alt) and travel to 
an ending (lat, lon, alt) in a straight line.
'''

import time
import numpy as np
from copter_control import CopterControl

def diag_line((lat0, lon0, alt0), (lat, lon, alt), k=10):
	"""
	return a path for the drone to follow
	"""
	lats = np.linspace(lat0, lat, k)
	lons = np.linspace(lon0, lon, k)
	alts = np.linspace(alt0, alt, k)
	return zip(lats, lons, alts)


start = (40.345767, -74.649985, 15)
end = (40.346005, -74.650118, 30)

path = diag_line(start, end)

# Initialize the copter connection
api = local_connect()
cc = CopterControl(api)

# arm copter
cc.arm()

# change to guided mode
cc.set_mode("GUIDED")

# wait for changes to take effect
time.sleep(2)

# takeoff!
print "Taking off ..."
cc.takeoff(15)
time.sleep(10)

# start following the path
print "Following path ..."
for p in path:
	cc.goto((p[0], p[1]), p[3])
	time.sleep(1.5)
