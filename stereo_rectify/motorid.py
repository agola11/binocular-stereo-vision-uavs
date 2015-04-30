import log_reader as lr
import numpy as np
import matplotlib.pyplot as plt

fname = "c:\\Users\\Joseph\Videos\\Flight With Ball\\MotorID.log"
#t0 =  75850
t0 = 126900
tspan = 146150-t0
#t0 = 92000
#tspan = 96000-92000
f = 50.      #50 Hz sampling rate
g = 9.8
m = 3.       #kg. Fix this.

reader = lr.LogReader(fname,-343.67)
t_ms = np.linspace(t0, t0+tspan, tspan*f/1000)
t_s = t_ms/1000.

motor_vals = reader.get_motor_vals(t_ms)

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
#plt.legend(handles=[l0,l1,l2,l3,l4,l5,l6,l7])
plt.show()
