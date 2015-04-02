from __future__ import print_function
import time, sys
from copter_control import CopterControl

# DroneAPI APIConnection
api = local_connect()
cc = CopterControl(api)

f = open('attitude.log', 'w')

start = time.time()
dur = 120.0
while True:
	now = time.time()
	diff = now-start
	if diff >= dur:
		break
	attitude = cc.get_attitude()
	print(str(diff) + ": " + str(attitude))
	print(str(diff) + ": " + str(attitude), file=f)
	time.sleep(0.1)

f.close()

