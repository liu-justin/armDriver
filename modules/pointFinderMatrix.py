import basicShapes as bs
import stepMath as smath
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

ORIGIN = np.array([0,0,0])





# plug in the angle, regular CCW from 0 to the right

# got from solidworks skeleton main, when RO-RR is vertical and RR is 0,0
RO = np.array([0, 0, 2.5])
RA = np.array([-2.40315424, 0, 3.18909339])
RC = np.array([6.99893387, 0, 2.37783316])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i in np.arange(0, 50*1.8*np.pi/180, 5*1.8*np.pi/180):
    # rotation theta
    angleRT = np.pi/6
    A_RT = np.array([[ np.cos(angleRT), -np.sin(angleRT), 0],
                     [np.sin(angleRT) , np.cos(angleRT) , 0],
                     [0               , 0               , 1]])

    angleRR = i
    A_RR = np.array([[np.cos(angleRR) , 0, np.sin(angleRR)],
                     [0               , 1,               0],
                     [-np.sin(angleRR), 0, np.cos(angleRR)]])

    RO_new = np.dot(A_RT, np.dot(A_RR, RO))
    RA_new = np.dot(A_RT, np.dot(A_RR, RA))
    RC_new = np.dot(A_RT, np.dot(A_RR, RC))

    print(f"RO: {RO_new}, RA: {RA_new}, RC: {RC_new}")

    plotting_array = np.array([ORIGIN, RO_new, RA_new, RO_new, RC_new, RO_new, ORIGIN])
    ax.plot3D(plotting_array[:,0], plotting_array[:,1], plotting_array[:,2])


ax.set_xlabel('X (in)')
ax.set_ylabel('Y (in)')
ax.set_zlabel('Z (in)')

plt.show()