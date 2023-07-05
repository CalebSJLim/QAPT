import numpy as np
import matplotlib.pyplot as plt
import itertools as it
from matplotlib.widgets import Slider, Button

plt.rcParams['figure.dpi'] = 100
plt.rcParams.update({'font.size': 10})

# theta: angle
# theta_dot: angular velocity
# theta_ddot: angular acceleration
# mu: air resistance term (between 0 and 1)
L = 1
g = 9.81
theta_dot = 2.5
theta_dot_0 = theta_dot
theta = np.pi/2
theta_0 = theta

angles = []
angular_vels = []

def theta_ddot(theta, theta_dot):
    return - g * np.sin(theta) / L

dt = 0.001
t = np.arange(0, 10, dt)

for time in t:
    theta_dot += dt * theta_ddot(theta, theta_dot)
    theta += dt * theta_dot
    
    angles.append(theta)
    angular_vels.append(theta_dot)


fig, axs = plt.subplots(2, 2)
fig.tight_layout()

t = np.array(t)


axs[0, 0].plot(t, np.array(angles), color="blue")
axs[0, 0].set_title("Graph of Angles against Time")
axs[0, 0].set_xlabel("Time/s")
axs[0, 0].set_ylabel("Angle/rad")

axs[1, 0].plot(t, angular_vels, color="orange")
axs[1, 0].set_title("Graph of Angular Velocity against Time")
axs[1, 0].set_xlabel("Time/s")
axs[1, 0].set_ylabel("Angular Velocity/(rad/s)")

x = np.linspace(0, 2*np.pi, 15)
y = np.linspace(0, 2*np.pi, 15)
x, y = np.meshgrid(x, y)

v_x = y
v_y = theta_ddot(x, y)
vec_field = axs[0, 1].quiver(x, y, v_x/np.sqrt(v_x**2 + v_y**2), v_y/np.sqrt(v_x**2 + v_y**2), np.sqrt(v_x**2 + v_y**2), cmap="plasma")
axs[0, 1].set_title("Phase Space")
axs[0, 1].set_xlabel("Angle")
axs[0, 1].set_ylabel("Angular Velocity")
cbar1 = plt.colorbar(vec_field, ax=axs[0, 1])
cbar1.ax.set_ylabel("Arrow Length")

def intersect(x, y):
    vals = []
    
    for th, th_dot in it.product(x, y):
        args = []
        
        for time in t:
            th_dot += dt * theta_ddot(th, th_dot)
            th += dt * th_dot
            args.append(float(th))

        ma = max(args)
        mi = min(args)

        if (ma >= 0) and (mi <= 0):
            vals.append(1)
        else:
            vals.append(0)

    return vals
    
X = np.linspace(-4*np.pi, 4*np.pi, 50)
Y = np.linspace(-15, 15, 35)
Z = np.array(intersect(X, Y)).reshape(len(X), len(Y))

X, Y = np.meshgrid(X, Y)
fall_over = axs[1, 1].pcolormesh(Z, cmap='cividis')
axs[1, 1].set_title("Does it cross the horizontal?")
axs[1, 1].set_xlabel("Initial Angle")
axs[1, 1].set_ylabel("Initial Angular Velocity")
cbar2 = plt.colorbar(fall_over, ax=axs[1, 1])
cbar2.ax.set_ylabel("Does it cross the horizontal?")

plt.show()
