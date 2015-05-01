#!/usr/bin/python

import numpy as np
from log_reader import LogReader
from filterpy.kalman import UnscentedKalmanFilter as UKF

START_TIME = 254000 # ms
END_TIME = 268200 # ms
dt = 1000.0/30 # ms
fx_times = 1

def get_R(att):
    #att = np.deg2rad(att)
    r_pitch = np.array([[ np.cos(att[1]), 0, -np.sin(att[1])],
                        [              0, 1,               0],
                        [ np.sin(att[1]), 0,  np.cos(att[1])]])
    r_roll = np.array([[1,               0,              0],
                       [0,  np.cos(att[0]), np.sin(att[0])],
                       [0, -np.sin(att[0]), np.cos(att[0])]])
    r_yaw = np.array([[ np.cos(att[2]), np.sin(att[2]), 0],
                      [ -np.sin(att[2]), np.cos(att[2]), 0],
                      [              0,              0, 1]])
    R = r_roll.dot(r_pitch.dot(r_yaw))
    return R

def hx(x):
	"""
	return the measurement of the state
	"""
	C = np.eye(12)
	C[9, 9] = 0
	C[9, 0] = 1
	C[10, 10] = 0
	C[10, 1] = 1
	C[11, 11] = 0
	C[11, 2] = 1
	return C.dot(x)

def fx(x, dt):
	"""
	return the state transformed by the state transition function
	dt is in seconds
	"""
	global left_reader
	global START_TIME
	global fx_times
	m = 2.9 # mass in kg
	l = .1516 # length of quadcopter rotor in
	w = .2357
	I_x = .3789
	I_y = .06193
	k_i_2 = .00009876
	k1 = .0092
	g = 9.8


	dt_ms = dt * 1000
	mi = left_reader.get_motor_inputs(START_TIME+(dt_ms*fx_times))
	mi = mi - 1143 # important
	R = get_R([x[6], x[7], x[8]])
	R_inv = np.linalg.inv(R)

	F = mi.sum() *k1


	pos_dots = R_inv.dot(np.array([x[3], x[4], x[5]])) # x_dot, y_dot, z_dot
	
	u_dot = -g * np.sin(x[7])
	v_dot = g * np.cos(x[7]) * np.sin(x[6]) 
	w_dot = g * np.cos(x[7]) * np.cos(x[6]) - (F/m)

	R_att = np.array([[1, np.sin(x[6])*np.tan(x[7]), np.cos(x[6])*np.tan(x[7])],
					  [0, np.cos(x[6]), -np.sin(x[6])],
					  [0, np.sin(x[6])*(1.0/np.cos(x[7])), np.cos(x[6])*(1.0/np.cos(x[7]))]])

	att_dots = R_att.dot(np.array([x[9], x[10], x[11]]))

	# torque around phi
	t_phi = np.array([-w*k1, w*k1, -w*k1, w*k1, -w*k1, w*k1, -w*k1, w*k1]).dot(mi)
	t_theta = np.array([l*k1, l*k1, -l*k1, -l*k1, l*k1, l*k1, -l*k1, -l*k1]).dot(mi)
	t_psi = np.array([k_i_2, -k_i_2, -k_i_2, k_i_2, -k_i_2, k_i_2, k_i_2, -k_i_2]).dot(mi)

	r_dot = t_psi
	p_dot = t_phi/I_x
	q_dot = t_theta/I_y

	state_dot = np.array([pos_dots[0], pos_dots[1], pos_dots[2], u_dot, v_dot, w_dot, att_dots[0], att_dots[1], att_dots[2], p_dot, q_dot, r_dot])

	new_state = x + state_dot*dt
	fx_times +=1

	return new_state

ukf = UKF(dim_x=12, dim_z=12)

"""
Log stuff
"""
vid_fname = "c:\\Users\\Joseph\\Documents\\14-15\\Thesis\\SeniorThesis2015\\ball_tracker\\svm\\videos\\output.mp4"

l_fname = "c:\\Users\\Joseph\Videos\\Flight With Ball\\Left.MP4"
l_logname = "c:\\Users\\Joseph\Videos\\Flight With Ball\\Left.log"
l_rect_start_time_ms = 259000
l_first_data_time_ms = 14414.4

stereo_offset = (14481.133 - 14414.4)

r_fname = "c:\\Users\\Joseph\Videos\\Flight With Ball\\Right.MP4"
r_logname = "c:\\Users\\Joseph\Videos\\Flight With Ball\\Right.log"
r_rect_start_time_ms = l_rect_start_time_ms + int(stereo_offset)
r_first_data_time_ms = 31064.366

C920_data = np.load("C920_calib_data.npz")
F = C920_data['intrinsic_matrix']
track_fname = "super_ball_track.log"
track_offset = 30230   #tracking log is ~29998 ms behind left gopro
track_data_log_offset = track_offset + stereo_offset

left_reader = lr.LogReader(l_logname,l_first_data_time_ms)
right_reader = lr.LogReader(r_logname,r_first_data_time_ms)

track = tr.TrackingReader(track_fname,right_reader,track_data_log_offset,F,30,1,vid_fname=vid_fname)

