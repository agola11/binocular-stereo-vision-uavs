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


start = (40.345845, -74.650027, 15) # football field
end = (40.345990, -74.650127, 30) # football field

'''
start = (40.345344, -74.647786) # practice field 50
end = (40.345112, -74.647657) # practice field 25
'''

'''
start = (40.344641, -74.649337) # track mid
end = (40.344448, -74.649908) # track end
'''

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
