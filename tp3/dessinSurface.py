from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np


xi = np.linspace( 0., 1., num=10)
yj = np.linspace( 0., 1., num=10)

X, Y = np.meshgrid( xi, yj)

Z = np.sin(X**2 + Y**2) / ((X**2 + Y**2) + 1.)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Grab some test data.
#X, Y, Z = axes3d.get_test_data(0.05)

# Plot a basic wireframe.
ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)

plt.show()
