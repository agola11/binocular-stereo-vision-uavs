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

def at_loc((x, y), (cx, cy), eps=.00003):
	"""
	check if current lat, lon (x, y) is within eps of target lat, lon (cx, cy)
	"""
	return (x - cx)**2 + (y - cy)**2 <= eps**2



def diag_line((lat0, lon0, alt0), (lat, lon, alt), k=5):
	"""
	return a path for the drone to follow
	"""
	lats = np.linspace(lat0, lat, k)
	lons = np.linspace(lon0, lon, k)
	alts = np.linspace(alt0, alt, k)
	p = zip(lats, lons, alts)
	return p


#start = (40.345845, -74.650027, 15) # football field
#end = (40.345990, -74.650127, 30) # football field

start = (40.345652, -74.650070, 15) # 40
end = (40.345797, -74.650172, 15) # 20

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
time.sleep(3)

# takeoff!
print "Taking off ..."
cc.takeoff(15)
time.sleep(10)

# going to start location
print "going to start loc"
cc.goto((start[0], start[1]), start[2])
cc.set_yaw(250)
time.sleep(10)

# start following the path
print "Following path ..."
for p in path[1:]:
	print "GOING TO ", p
	cc.goto((p[0], p[1]), p[2])
	while not at_loc((cc.get_current_location().lat, cc.get_current_location().lon), (p[0], p[1])):
		time.sleep(0.01)