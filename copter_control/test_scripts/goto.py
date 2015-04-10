import time
from droneapi.lib import VehicleMode, Location
from pymavlink import mavutil

api = local_connect()
v = api.get_vehicles()[0]
commands = v.commands


v.armed = True
v.flush()


alt = 30;

v.mode = VehicleMode("GUIDED")
v.flush()

time.sleep(3);

poe_wps = [(40.343762, -74.653822), (40.343750, -74.654158), (40.343519, -74.654493), (40.343547, -74.653938)]
foot_wps = [(40.345763, -74.649955), (40.346069, -74.650159), (40.345706, -74.649895), (40.345634, -74.649994)]


origin = Location(foot_wps[0][0], foot_wps[0][1], alt, is_relative=True)

print "GOING TO " + str(foot_wps[0]) + "..."

commands.goto(origin)
v.flush()

"""
# sleep 2 seconds so we can see the change in map
time.sleep(5)

destination = Location(poe_wps[1][0], poe_wps[1][0], 30, is_relative=True)

commands.goto(destination)
vehicle.flush()
"""