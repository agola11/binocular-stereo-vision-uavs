from droneapi.lib import VehicleMode
from pymavlink import mavutil
import time

# First get an instance of the API endpoint
api = local_connect()
# get our vehicle - when running with mavproxy it only knows about one vehicle (for now)
v = api.get_vehicles()[0]

v.mode = VehicleMode("RTL")
v.flush()
