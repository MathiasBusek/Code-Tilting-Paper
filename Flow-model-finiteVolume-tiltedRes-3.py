import numpy as np
import matplotlib.pyplot as plt

speed = 3           # in rpm
alpha = 20          # in deg
channel_length = 20 # in mm
viscosity=0.0008     # in Pa*s
density=1000        # in kg/m3
gravity=9.81        # in m/s2
channel_width=3.2     # in mm
channel_heigth=0.5  # in mm
res_width=3         # in mm
res_length=20       # in mm

volumes = [300, 500, 1100]       # Initial volume filled in the reservoirs

# Hydraulic resistance
R=(12*viscosity*channel_length/1000)/((np.power(channel_heigth/1000, 3)*channel_width/1000)*(1-0.63*(channel_heigth/channel_width)))

k = density*gravity / (R * 0.000001)
# angular frequency
omega = 2*np.pi*speed/60
# time step for simulation
delta_t = 0.001
stop_time = 40

dh_min = 1

fig, axs = plt.subplots(4, sharex=True)

def getHeigth(V, tilt):

    h_tilt = res_length * np.sin(tilt)
    h = V/(res_width * res_length)

    if(h < h_tilt):
        h = 0
    
    return h

def simulate(V):
    # timeseries for simulation
    t=np.linspace(0, stop_time, int(stop_time/delta_t))

    Q_1 = []    
    Q_2 = []

    V_1 = []
    V_2 = []

    V1 = V/2
    V2 = V/2

    for time in t:
    
        tilt_y = alpha/180*np.pi*(np.sin(omega*time))
        dh_tilt = channel_length*np.sin(tilt_y)

        tilt_z = alpha/180*np.pi*(np.sin(omega*time+np.pi/2))

        h1_r = getHeigth(V1, -tilt_z)
        h2_r = getHeigth(V2, -tilt_z)
        h1_l = getHeigth(V1, tilt_z)
        h2_l = getHeigth(V2, tilt_z)

        dh_1 = (dh_tilt + h1_r - h2_r)
        if(dh_1 > 0):
            if (h1_r == 0):
                dh_1 = 0
            if ((h2_r == 0) and (abs(dh_1) < dh_min)):
                dh_1 = 0
        else:
            if (h2_r == 0):
                dh_1 = 0
            if ((h1_r == 0) and (abs(dh_1) < dh_min)):
                dh_1 = 0

        dh_2 = (dh_tilt + h1_l - h2_l)
        if(dh_2 > 0):
            if (h1_l == 0):
                dh_2 = 0
            if ((h2_l == 0) and (abs(dh_2) < dh_min)):
                dh_2 = 0
        else:
            if (h2_l == 0):
                dh_2 = 0
            if ((h1_l == 0) and (abs(dh_2) < dh_min)):
                dh_2 = 0
                
        Q1 = dh_1*k
        Q2 = dh_2*k

        V1 = V1 - Q1*delta_t - Q2*delta_t
        if(V1 < 0):
            V1 = 0
 
        V2 = V2 + Q1*delta_t + Q2*delta_t
        if(V2 < 0):
            V2 = 0
    
        V_1.append(V1)
        V_2.append(V2)
        Q_1.append(Q1)
        Q_2.append(Q2)

    
    axs[0].plot(t, Q_1, label='Q1-'+str(V)+' uL')
    axs[1].plot(t, Q_2, label='Q2-'+str(V)+' uL')

    axs[2].plot(t, V_1, label='V1-'+str(V)+' uL')
    axs[3].plot(t, V_2, label='V2-'+str(V)+' uL')

for V in volumes:
    simulate(V)
    
axs[0].legend(loc='upper left')
axs[0].set(ylabel='Q [uL/s]')
axs[1].legend(loc='upper left')
axs[1].set(ylabel='Q [uL/s]')
axs[2].legend(loc='upper left')
axs[2].set(ylabel='V [uL]')
axs[3].legend(loc='upper left')
axs[3].set(xlabel = 't [s]', ylabel='V [uL]')
plt.show()
