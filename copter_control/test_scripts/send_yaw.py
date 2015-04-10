from droneapi.lib import VehicleMode
from pymavlink import mavutil

# First get an instance of the API endpoint
api = local_connect()
# get our vehicle - when running with mavproxy it only knows about one vehicle (for now)
v = api.get_vehicles()[0]
msg = v.message_factory.mission_item_encode(0, 0,  # target system, target component
                                                     0,     # sequence
                                                     mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, # frame
                                                     mavutil.mavlink.MAV_CMD_CONDITION_YAW,         # command
                                                     2, # current - set to 2 to make it a guided command
                                                     0, # auto continue
                                                     90, 0, 0, 0, 0, 0, 0) # param 1 ~ 7
# send command to vehicle
v.send_mavlink(msg)
v.flush()