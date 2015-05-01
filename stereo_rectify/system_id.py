import log_reader as lr
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

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

fname = "c:\\Users\\Joseph\Videos\\Flight With Ball\\Ball_sysid.log"
#fname = "c:\\Users\\Joseph\Videos\\Flight With Ball\\Right.log"
t0 =  58000
#t0 = 186500
tspan = 160000 - t0
#tspan = 12000
#t0 = 92000
#tspan = 96000-92000
f = 50.      #50 Hz sampling rate
g = 9.8
m = 2.9      #kg. Fix this.
w = 0.2357
l = 0.1516

reader = lr.LogReader(fname,-343.67)
t_ms = np.linspace(t0, t0+tspan, tspan*f/1000)
t_s = t_ms/1000.

gyr = reader.get_gyr(t_ms)
pos = reader.get_ekf_loc_1d(t_ms)
att = np.deg2rad(reader.get_ekf_att(t_ms))
motor_vals = reader.get_motor_vals(t_ms)
motor_vals = motor_vals - 1143          # THIS IS IMPORTANT. 1190 for Camera quad.
motor_means = np.mean(motor_vals,axis=1)
ned_vel = reader.get_ekf_vel(t_ms)
body_vel = np.zeros(ned_vel.shape)
for i in range(0,t_ms.shape[0]):
    R = get_R(att[:,i])
    body_vel[:,i] = R.dot(ned_vel[:,i])

b,a = sig.iirfilter(4,.3,btype = 'lowpass')
body_acc = np.diff(body_vel,axis=1)*f
filtered_acc = sig.lfilter(b,a,body_acc,axis=1)
sumd = np.sum(motor_vals,axis=0)
acc_adj = body_acc[2,:] - (g*np.cos(att[1,:])*np.cos(att[0,:]))[0:-1]
k1 = -m*acc_adj/sumd[0:-1]
print k1.shape, np.mean(k1)
k1 = 0.00922

b,a = sig.iirfilter(4,.3,btype = 'lowpass')
#att = sig.lfilter(b,a,att,axis=1)
att_vel = np.diff(att,axis=1)*f
att_acc = np.diff(att_vel,axis=1)*f
gyr_acc = np.diff(gyr,axis=1)*f
roll_torques = k1*np.array([-w,w,-w,w,-w,w,-w,w]).dot(motor_vals)
Ix = roll_torques[0:-1]/gyr_acc[0,:]
print Ix.shape, np.mean(Ix)

pitch_torques = k1*np.array([l,l,-l,-l,l,l,-l,-l]).dot(motor_vals)
Iy = pitch_torques[0:-1]/gyr_acc[1,:]
print Iy.shape, np.mean(Iy)

yaw_torques = np.array([1,-1,-1,1,-1,1,1,-1]).dot(motor_vals)
param = gyr_acc[2,:]/yaw_torques[0:-1]
print param.shape, np.mean(param)

plt.figure(1)
plt.scatter(roll_torques[0:-1], gyr_acc[0,:])
plt.plot(np.array([-1.5,2]),1/np.mean(Ix)*np.array([-1.5,2]),label='Ix fit')
plt.xlabel('Roll Torque')
plt.ylabel('Roll Acceleration')
plt.legend()

plt.figure(2)
plt.scatter(pitch_torques[0:-1], gyr_acc[1,:])
plt.plot(np.array([-2,1]),1/np.mean(Iy)*np.array([-2,1]),label='Iy fit')
plt.xlabel('Pitch Torque')
plt.ylabel('Pitch Acceleration')
plt.legend()

plt.figure(4)
plt.scatter(yaw_torques[0:-1], gyr_acc[2,:],marker='.')
plt.plot(np.array([-2000,2000]),np.mean(param)*np.array([-2000,2000]),label='K2/Iz fit')
plt.xlabel('Yaw Motor Sum')
plt.ylabel('Yaw Acceleration')
plt.legend()

plt.figure(3)
plt.scatter(sumd[0:-1],-m*acc_adj,marker='.')
l = plt.plot(np.array([0,5000]),np.mean(k1)*np.array([0,5000]),label = 'k1 fit')
plt.legend()
plt.axis([0,5500,0,80])
plt.xlabel('Sum of Motor Inputs')
plt.ylabel('Observed Force on X8')

plt.show()
