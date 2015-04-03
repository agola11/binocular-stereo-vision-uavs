from __future__ import print_function
import time, sys
from copter_control import CopterControl

# DroneAPI APIConnection
api = local_connect()
cc = CopterControl(api)

f = open('attitude.log', 'w')

start = time.time()
dur = 120.0
prev_yaw = -1.0

while True:
	now = time.time()
	diff = now-start
	if diff >= dur:
		break
	attitude = cc.get_attitude()
	yaw = attitude.yaw
	if prev_yaw != yaw:
		print(str(diff) + ": " + str(yaw))
		print(str(diff) + ": " + str(yaw), file=f)
		prev_yaw = yaw

f.close()

