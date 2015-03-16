from droneapi.lib import VehicleMode
from pymavlink import mavutil
import time

# First get an instance of the API endpoint
api = local_connect()
# get our vehicle - when running with mavproxy it only knows about one vehicle (for now)
v = api.get_vehicles()[0]

print "Armed: %s" % v.armed
v.flush()

v.armed = True
v.flush()

v.mode = VehicleMode("AUTO")
v.flush()

time.sleep(5)

print "NAME = " + v.mode.name
channel = "1"

vals = range(10, 1500, 100)

print "OVERRIDING CHANNEL " + channel
i = 0


while v.mode.name == "AUTO" and i < len(vals):
	print "VALUE = " + str(vals[i])
	v.channel_override = { channel : vals[i]}
	i+=1
	time.sleep(2)


# gain back control of channel
v.channel_override = {channel: 0}