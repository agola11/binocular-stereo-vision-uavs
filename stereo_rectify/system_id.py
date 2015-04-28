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

fname = "c:\\Users\\Joseph\Videos\\Flight With Ball\\sysid.log"
#fname = "c:\\Users\\Joseph\Videos\\Flight With Ball\\Right.log"
t0 =  80000
#t0 = 186500
tspan = 120000
#t0 = 92000
#tspan = 96000-92000
f = 50.      #50 Hz sampling rate
g = 9.8
m = 3.2      #kg. Fix this.

reader = lr.LogReader(fname,-343.67)
t_ms = np.linspace(t0, t0+tspan, tspan*f/1000)
t_s = t_ms/1000.

pos = reader.get_ekf_loc_1d(t_ms)
att = np.deg2rad(reader.get_ekf_att(t_ms))
motor_vals = reader.get_motor_vals(t_ms)
motor_vals = motor_vals - 1190          # THIS IS IMPORTANT
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

plt.figure(1)
l0=plt.plot(t_s, motor_vals[0,:],label='0')
l1=plt.plot(t_s, motor_vals[1,:],label='1')
l2=plt.plot(t_s, motor_vals[2,:],label='2')
l3=plt.plot(t_s, motor_vals[3,:],label='3')
l4=plt.plot(t_s, motor_vals[4,:],label='4')
l5=plt.plot(t_s, motor_vals[5,:],label='5')
l6=plt.plot(t_s, motor_vals[6,:],label='6')
l7=plt.plot(t_s, motor_vals[7,:],'o',label='7')
plt.legend()

plt.figure(2)
plt.plot(t_s,body_vel[2,:])
plt.plot(t_s,pos[2,:])
plt.plot(t_s[0:-1],body_acc[2,:])
plt.plot(t_s[0:-1],filtered_acc[2,:])

plt.figure(3)
plt.scatter(sumd[0:-1],-m*acc_adj,marker='.')
l = plt.plot(np.array([0,5000]),np.mean(k1)*np.array([0,5000]),label = 'k1 fit')
plt.legend()
plt.axis([0,5500,0,80])
plt.xlabel('Sum of Motor Inputs')
plt.ylabel('Observed Force on X8')

plt.show()
