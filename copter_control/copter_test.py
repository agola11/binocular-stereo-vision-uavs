"""
TESTING
"""

import time
from copter_control import CopterControl

def test():
	api = local_connect()
	cop_ctrl = CopterControl(api)

	print "ARMED = " + str(cop_ctrl.is_armed())

	
	cop_ctrl.arm()

	print "MODE = " + str(cop_ctrl.get_mode_name()) # should be stabilize if copter has just been turned on

	cop_ctrl.set_mode("GUIDED")
	time.sleep(2) # wait for changes to take effect
	print cop_ctrl.get_mode_name()
	
	"""
	origin = (40.345763, -74.649955)
	thirty = (40.345967, -74.650021)
	forty = (40.345712, -74.649880)

	print "TAKING OFF!"
	cop_ctrl.takeoff(15)
	time.sleep(15)

	
	print "SENDING VELOCITY COMMAND"
	cop_ctrl.set_velocity(1, 0, 0)
	time.sleep(10)
	cop_ctrl.set_velocity(0, 0, 0)
	"""


	"""
	print "GOING TO ORIGIN"
	cop_ctrl.goto(origin, 30) # fly to 50 yd line, 20m high
	time.sleep(4) # wait for changes to take effect

	
	cop_ctrl.set_yaw(270) # turn the copter due east
	time.sleep(30) # wait

	print "GOING TO FORTY"
	cop_ctrl.goto(forty, 60)


	cop_ctrl.set_yaw(90) 
	time.sleep(1)

	cop_ctrl.set_velocity(0.5, 0, 0)
	time.sleep(2)
	cop_ctrl.set_velocity(0, 0, 0)
	"""

test()