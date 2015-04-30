'''
copter_control.py
Author: 
	Ankush Gola, Joseph Bolling
'''

import time
from pymavlink import mavutil
from droneapi.lib import VehicleMode, Location

class CopterControl(object):
	"""
	CopterControl is a wrapper class for droneapi.lib.Vehicle that
	includes added control functionality

	This class is heavily adapted from Randy Mackay's VehicleControl class
	(rmackay on GitHub, project: SmartCamera)
	"""

	def __init__(self, api, vel_update=1):
		"""
		return an instance of CopterControl
		api: an APIConnection instance created by calling local_connect in parent file
		"""
		assert api is not None

		v = api.get_vehicles()[0]
		
		self.api = api
		self.uav = v
		self.vel_update = vel_update # TODO: velocity update rate

	def get_mode_name(self):
		"""
		return the name of current mode
		"""
		return self.uav.mode.name

	def get_mode(self):
		"""
		return the current VehicleMode
		"""
		return self.uav.mode

	def set_mode(self, mode):
		"""
		set the mode of the vehicle
		mode: the name of the mode
		"""
		self.uav.mode = VehicleMode(mode)
		self.uav.flush()

	def return_to_launch(self):
		"""
		make the uav return to the launch site
		"""
		self.uav.mode = VehicleMode("RTL")
		self.uav.flush()

	def land_here(self):
		"""
		make the uav land at the current location
		USE WITH CAUTION
		"""
		self.uav.mode = VehicleMode("LAND")
		self.uav.flush()

	def get_current_location(self):
		"""
		return the vehicle's current location (lat, lon, alt)
		"""
		return self.uav.location

	def get_velocity(self):
		"""
		return the vehicle's current velocity vector as a list: [vx, vy, vz] in m/s
		"""
		return self.uav.velocity

	def get_attitude(self):
		"""
		return the uav's current pitch, yaw, and roll
		"""
		return self.uav.attitude

	def takeoff(self, alt):
		"""
		takeoff to the desired altitude
		"""
		if self.uav.mode.name == "GUIDED":
			self.uav.commands.takeoff(alt)
			self.uav.flush()
			return True
		else:
			return False

	def get_copter(self):
		"""
		return the Vehicle instance
		"""
		return self.uav

	def is_armed(self):
		"""
		return True if vehicle is armed else False
		"""
		return self.uav.armed

	def arm(self):
		"""
		arm the vehicle 
		"""
		if not self.uav.armed:
			self.uav.armed = True
			self.uav.flush()

	def get_attitude(self):
		"""
		get the vehicle's attitude
		"""
		return self.uav.attitude

	def set_yaw(self, heading):
		"""
		set the yaw of the uav by sending condition_yaw in mavlink
		heading is in degrees, corresponding to a clockwise rotation
		"""

		'''
		TODO
		Only let commands through at 10hz
		'''
		msg = self.uav.message_factory.mission_item_encode(0, 0,  # target system, target component
														0,     # sequence
														mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, # frame
														mavutil.mavlink.MAV_CMD_CONDITION_YAW,         # command
														2, # current - set to 2 to make it a guided command
														0, # auto continue
														heading, 10, -1, 0, 0, 0, 0) # param 1 ~ 7

		# send command to vehicle
		self.uav.send_mavlink(msg)
		self.uav.flush()

	def set_velocity(self, v_x, v_y, v_z):
		"""
		set the velocity of the vehicle by sending raw mavlink
		velocity is in m/s
		"""

		'''
		TODO
		Only let commands through at 10hz
		'''
		msg = self.uav.message_factory.set_position_target_local_ned_encode(
														0,       # time_boot_ms (not used)
														255, 0,    # target system, target component
														mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
														0x01C7,  # type_mask (ignore pos | ignore acc)
														0, 0, 0, # x, y, z positions (not used)
														v_x, v_y, v_z, # x, y, z velocity in m/s
														0, 0, 0, # x, y, z acceleration (not used)
														0, 0)    # yaw, yaw_rate (not used)
		# send command to vehicle
		self.uav.send_mavlink(msg)
		self.uav.flush()

	def goto(self, (lat, lon), alt=30):
		"""
		send the uav to the designated latitude, longitude, and altidude.
		USE WITH CAUTION
		requires GPS lock
		"""
		if self.uav.mode.name == "GUIDED":
			loc = Location(lat, lon, alt, is_relative=True)
			self.uav.commands.goto(loc)
			self.uav.flush()
			return True

		return False


MESSAGES = {'armed':'ARMED', 'reached_alt':'REACHED_ALT'}