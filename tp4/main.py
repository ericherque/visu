from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import sys
import math

##Authors: 		BUISINE 	Julien
#				GEITNER 	Teva
#				HERQUE		Eric

#	La fonction évaluant Xi nous renvoie bien F(Xi) = fi, pour tout les Xi 
#	Cependant, la variation des µ_i n'influence pas le tracé final (problème)

#	PS: Le programme est très long à exécuter car pour chaque calcul de dénominateur
#		il y a 100*99 tour de boucle, on calcule 100 dénominateurs au total donc 990.000 tours
#		le tout avec des fonctions mathématiques python

# fonction retournant le résultat de la distance entre les points
# (x1, y1) et (x2, y2)
def distance(x1, x2, y1, y2):
	return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))


## (x,y) = le point qu'on a choisi
## X = tableau des x
## Y = tableau des y
## i = l'indice i de Wi
## mu = tableau des valeurs mu
def numerator_calcul(x, y, X, Y, i, mu):
	res = 1
	index = 0
	for (tabX, tabY) in zip(X, Y):
		for (eltX, eltY) in zip(tabX, tabY):
			if index != i:
				res *= math.pow(distance(x, eltX, y, eltY), mu[index])
			index += 1
	return res


## (x,y) = le point qu'on a choisi
## X = tableau des x
## Y = tableau des y
## i = l'indice i de Wi
## mu = tableau des valeurs mu
def denominator_calcul(x, y, X, Y, i, mu):
	res = 0
	X_array = []
	Y_array = []
	#init des tab de X et Y
	for (tabX, tabY) in zip(X, Y):
		for (eltX, eltY) in zip(tabX, tabY):
			X_array.append(eltX)
			Y_array.append(eltY)
	#calcul du dénominateur
	for j in range(0, len(X_array)):
		mult_inter = 1
		for k in range(0, len(X_array)):
				if j!=k:
					mult_inter *= math.pow(distance(x, X_array[k], y, Y_array[k]), mu[k])

		res += mult_inter
	return res

## calcul du poids Wi
def pointweight(x, y, X, Y, i, mu):
	numerator = numerator_calcul(x, y, X, Y, i, mu)
	denominator = denominator_calcul(x, y, X, Y, i, mu)
	return numerator/denominator

## fonction évaluant  un point (x,y) donné
def shepard(x, y, X, Y, values, mu):
	#somme de {wi(X) * fi}
	F = 0
	w = 0

	## récupération des valeurs Z
	Z_array = []
	for tab in values:
		for eltZ in tab:
			Z_array.append(eltZ)

	## on calcule Wi, puis on le multiplie à la valeur fi (Z[i])
	for i in range(0, len(Z_array)):
		w = pointweight(x, y, X, Y, i, mu)
		w *= Z_array[i]
		F += w
	return F
######
# Dessin surface
xi = np.linspace( 0., 1., num=10)
yj = np.linspace( 0., 1., num=10)

X, Y = np.meshgrid( xi, yj)

Zf = np.cos(X/2.) * np.sin(X**2 + Y)

## création d'un tableau de mu, avec des mu allant de 1 à 3
mu_test = np.zeros(len(X)*10)
for i in range(0, len(X)*10):
	if i %3 == 0 :
		mu_test[i] =1
	elif i %3 == 1 :
		mu_test[i] =5
	else :
		mu_test[i] =2

# EVALUER ZF
# EVALUER F( X(i,j), Y(i j) pour tout (i,j))
#
# On créée un tableau de 10 sous-tableaux de 10 valeurs (random)
#
# Puis à chaque tour de boucle nous insérons aux index [i,j] la valeur F 
# calculée pour le point X[i,j], Y[i,j]
#
F_array = np.zeros([10, 10], dtype = float)
print("Début du calcul...")
for i in range(len(X)):
	for j in range(len(Y)):
		F = shepard(X[i,j], Y[i,j], X, Y, Zf, mu_test)
		#print("i: ", i, "y: ", j, "Z: ", Zf[i,j], "F: ", F) 
		F_array[i,j] = F
	#print("F: ", F_array)
	print("Chargement: ", 10*(i+1), "%...")
print("Fin du calcul.")

for i in range(len(X)):
	for j in range(len(Y)):
		assert F_array[i,j] == Zf[i,j]

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
