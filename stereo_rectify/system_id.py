import log_reader as lr
import numpy as np
import matplotlib.pyplot as plt

fname = "c:\\Users\\Joseph\Videos\\Flight With Ball\\sysid.log"
t0 =  75850
tspan = 120000
f = 50      #50 Hz sampling rate

reader = lr.LogReader(fname,-343.67)
t = np.linspace(t0, t0+tspan, tspan*f/1000)

motor_vals = reader.get_motor_vals(t)
#for i in t[1:-1]:
#    print i
#    m = reader.get_motor_vals(i)
#    print motor_vals.shape, m.shape
#    motor_vals = np.vstack((motor_vals,m))

plt.figure(1)
plt.plot(t, motor_vals[0,:])
plt.show()