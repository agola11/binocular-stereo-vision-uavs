from __future__ import print_function
import time, sys
from pymavlink import mavutil
from droneapi.lib import VehicleMode, Location

# DroneAPI APIConnection
api = local_connect()
v = api.get_vehicles()[0]

f = open('attitude.log', 'w')

start = time.time()
dur = 30.0
while True:
	now = time.time()
	if now-start >= dur:
		break
	attitude = v.attitude
	print(attitude)
	print(attitude, file=f)
	time.sleep(0.1)

f.close()