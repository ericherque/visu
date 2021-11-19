from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import sys
import math

def distance(p1, p2):
	return math.sqrt(pow(p2[1] - p1[1], 2) + pow(p2[0] - p1[0], 2))

def distance2(x1, x2, y1, y2):
	return math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))


def numerator_calcul(x, y, X, Y, i, mu):
	## (x,y) = le point qu'on a choisi
	## X = tableau des x
	## Y = tableau des y
	## i = l'indice i de Wi
	## mu = pour l'instant on met une valeur fixe
	res = 1
	index = 0
	for (tabX, tabY) in zip(X, Y):
		for (eltX, eltY) in zip(tabX, tabY):
			if index != i:
				res *= pow(distance2(x, eltX, y, eltY), mu)
	return res

def denominator_calcul(x, y, X, Y, i, mu):
	res = 0
	mult_inter = 1
	X_array = []
	Y_array = []
	index = 0
	## init
	for (tabX, tabY) in (X, Y):
		for (eltX, eltY) in (tabX, tabY):
			X_array[index] = eltX
			Y_array[index] = eltY
			index += 1

	for j in range(0, len(X_array)-1):
		for k in range(0, len(X_array)-1):
				if j!=k:
					mult_inter *= pow(distance2(x, X_array[k], y, Y_array[k]), mu)
			
		res += mult_inter
	return res


def pointweight(x, y, X, Y, i, mu):
	numerator = numerator_calcul(x, y, X, Y, i, mu)
	denominator = denominator_calcul(x, y, X, Y, i, mu)
	return numerator/denominator


def pointweight_old(X, Y, i, x, y, mu):

	numerator = 1
	denominator = 0

	for k in range(0, len(x[0])-1):
		# résultat de la multiplication (pour dénominateur)
		mult_inter = 1

		# calcul du numérateur sans k=i
		if k!=i:
			numerator *= pow(distance2(X, x[k], Y, y[k]), mu[k])

		#calcul du dénominateur sans k=j
		for j in range(0, len(x)-1):
			if j!=k:
				mult_inter *= pow(distance2(X, x[j], Y, y[j]), mu[j])
		
		denominator += mult_inter
				
	return numerator/denominator


def shepard(X, Y, x, y, values, mu):
	#somme de {wi(X) * fi}
	F = 0
	w = 0
	Z_array = []
	for tab in values:
		for eltZ in tab:
			Z_array.append(eltZ)

	for i in range(0, len(x)-1):
		w = pointweight(X, Y, i, x, y, mu)
		w *= Z_array[i]
		F += w
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
shepard(x_random, y_random, X, Y, Zf, 2)

#
#
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Grab some test data.
#X, Y, Z = axes3d.get_test_data(0.05)

# Plot a basic wireframe.
ax.plot_wireframe(X, Y, Zf, rstride=2, cstride=1)
ax.scatter( [0.2, 0.8, 0.1],[0.3, 0.5, 0.7],[0.5, 0.5, 0.5], marker="^")

ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')


plt.show()
