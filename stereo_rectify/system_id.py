import log_reader as lr
import numpy as np
import matplotlib.pyplot as plt

def get_R(att):
    r_pitch = np.array([[ np.cos(att[1]), 0, -np.sin(att[1])],
                        [              0, 1,               0],
                        [ np.sin(att[1]), 0,  np.cos(att[1])]])
    r_roll = np.array([[1,               0,              0],
                       [0,  np.cos(att[0]), np.sin(att[0])],
                       [0, -np.sin(att[0]), np.cos(att[0])]])
    r_yaw = np.array([[ np.cos(att[2]), np.sin(att[2]), 0],
                      [-np.sin(att[2]), np.cos(att[2]), 0],
                      [              0,              0, 1]])
    R = r_roll.dot(r_pitch.dot(r_yaw))
    return R

fname = "c:\\Users\\Joseph\Videos\\Flight With Ball\\sysid.log"
t0 =  75850
tspan = 120000
f = 50.      #50 Hz sampling rate
g = 9.8
m = 3.       #kg. Fix this.

reader = lr.LogReader(fname,-343.67)
t_ms = np.linspace(t0, t0+tspan, tspan*f/1000)
t_s = t_ms/1000.

pos = reader.get_ekf_loc_1d(t_ms)
att = reader.get_ekf_att(t_ms)
motor_vals = reader.get_motor_vals(t_ms)
ned_vel = reader.get_ekf_vel(t_ms)
body_vel = np.zeros(ned_vel.shape)
for i in range(0,t_ms.shape[0]):
    R = get_R(att[:,i])
    body_vel[:,i] = R.dot(ned_vel[:,i])
body_acc = np.diff(body_vel,axis=1)*f
sumd = np.sum(motor_vals,axis=0)
print sumd[0:-1].shape

#TODO: subtract gravitational acceleration or whatever.

plt.figure(1)
plt.plot(t_s, np.sum(motor_vals,axis=0))

plt.figure(2)
plt.plot(t_s,body_vel[2,:])
plt.plot(t_s,pos[2,:])

plt.figure(3)
plt.scatter(body_acc[2,:],sumd[0:-1])

plt.show()
