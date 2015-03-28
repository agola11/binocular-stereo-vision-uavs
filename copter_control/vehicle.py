'''
vehicle.py
Author:
	Ankush Gola, Joseph Bolling
'''

from pymavlink import mavutil
import time, threading, zmq, string, random

def id_gen(size=8, chars=string.ascii_uppercase + string.digits):
	"""
	Generate a random ID of length size, using digits and uppercase chars
	http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
	"""
	return ''.join(random.choice(chars) for _ in range(size))

def get_location():
	pass

class Vehicle:
	"""
	A Vehicle object is instantiated given a serial port for
	the telemetry link.
	"""

	def __init__(self, port, baud= 57600, name=id_gen):
		self.name = name
		self.master = mavutil.mavlink_connection(device=port, baud=baud, autoreconnect=False)
		self.lat = None
		self.lon = None
		self.alt = None
		self.thread = threading.Thread(target = self.update)
		self.thread.start()

	def display_loc(self):
		pass

	def update_loc(self):
		# thread
		pass

	def arm(self):
		# TODO: Check MODE
		self.master.arducopter_arm()

	def takeoff(self, alt=None):
		if alt == None:
			return 0
		else:
			self.master.motors_armed_wait() # wait for motors to become armed
			self.master.mav.command_long_send(self.master.target_system,
                                                    self.master.target_component,
                                                    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                                                    0, 0, 0, 0, 0, 0, 0,
                                                    float(alt))
			return 1


	"""
	motors armed wait
	"""


