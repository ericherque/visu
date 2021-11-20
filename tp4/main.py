from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import sys
import math

def distance(p1, p2):
	return math.sqrt(pow(p2[1] - p1[1], 2) + pow(p2[0] - p1[0], 2))

def distance2(x1, x2, y1, y2):
	return math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))


## (x,y) = le point qu'on a choisi
	## X = tableau des x
	## Y = tableau des y
	## i = l'indice i de Wi
	## mu = pour l'instant on met une valeur fixe
def numerator_calcul(x, y, X, Y, i, mu):
	res = 1
	index = 0
	for (tabX, tabY) in zip(X, Y):
		for (eltX, eltY) in zip(tabX, tabY):
			if index != i:
				res *= pow(distance2(x, eltX, y, eltY), mu)
			index += 1
	return res


## (x,y) = le point qu'on a choisi
## X = tableau des x
## Y = tableau des y
## i = l'indice i de Wi
## mu = pour l'instant on met une valeur fixe
def denominator_calcul(x, y, X, Y, i, mu, X_array, Y_array):
	res = 0
	#X_array = []
	#Y_array = []
	#calcul du dénominateur
	for j in range(0, len(X_array)):
		mult_inter = 1
		for k in range(0, len(X_array)):
				if j!=k:
					mult_inter *= pow(distance2(x, X_array[k], y, Y_array[k]), mu)

		res += mult_inter
	return res

def init_tab_x_y(X, Y):
	#init des tab de X et Y
	X_array = []
	Y_array = []
	for (tabX, tabY) in zip(X, Y):
		for (eltX, eltY) in zip(tabX, tabY):
			X_array.append(eltX)
			Y_array.append(eltY)
	return (X_array, Y_array)

def pointweight(x, y, X, Y, i, mu, X_array, Y_array):
	##calcul du Wi
	numerator = numerator_calcul(x, y, X, Y, i, mu)
	#print(numerator)
	denominator = denominator_calcul(x, y, X, Y, i, mu, X_array, Y_array)
	return numerator/denominator


def shepard(x, y, X, Y, values, mu):
	#somme de {wi(X) * fi}
	F = 0
	w = 0
	Z_array = []
	for tab in values:
		for eltZ in tab:
			Z_array.append(eltZ)
	(X_array, Y_array) = init_tab_x_y(X, Y)
	for i in range(0, len(Z_array)):
		w = pointweight(x, y, X, Y, i, mu, X_array, Y_array)
		w *= Z_array[i]
		F += w
	return F
######
# Dessin surface
xi = np.linspace( 0., 1., num=10)
yj = np.linspace( 0., 1., num=10)

X, Y = np.meshgrid( xi, yj)

Zf = np.cos(X/2.) * np.sin(X**2 + Y)
# EVALUER ZF
# EVALUER F( X(i,j), Y(i j) pour tout (i,j))
#
x_random = 2
y_random = 7
print(Zf)
F_array = np.empty((10,10),dtype = 'float64')
for i in range(len(X)):
	F_subarray = np.empty(10, dtype = 'float64')
	for j in range(len(Y)):
		F = shepard(X[i,j], Y[i,j], X, Y, Zf, 2)
		print("i: ", i, "y: ", j, "Z: ", Zf[i,j], "F: ", F)
		F_subarray[j] = F
	F_array[i] = F_subarray

print(F_array)
#print(Zf)
#
#
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Grab some test data.
#X, Y, Z = axes3d.get_test_data(0.05)

# Plot a basic wireframe.
ax.plot_wireframe(X, Y, Zf, rstride=2, cstride=1)
ax.plot_wireframe(X, Y, F_array, rstride=1, cstride=1, color="r")
ax.scatter( [0.2, 0.8, 0.1],[0.3, 0.5, 0.7],[0.5, 0.5, 0.5], marker="^")

ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')


plt.show()
