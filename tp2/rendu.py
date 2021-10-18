import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
import math

def decomposition(array) :
    x_array = []
    y_array = []
    size = len(array)

    for index in range(0, size-1):
        # x_i^n value
        value = 1/4 * ( (-array[((2*index)-2)%size] + 3*array[(2*index-1)%size] + 3*array[(2*index)%size] - array[((2*index)+1)%size] ))
        x_array.append([value[0],value[1]])

        # y_i^n value
        value = 1/4 * ( (array[((2*index)-2)%size] - 3*array[(2*index-1)%size] + 3*array[(2*index)%size] - array[((2*index)+1)%size] ))
        y_array.append([value[0],value[1]])
    res = np.concatenate([x_array, y_array])
    return res

def decompose(x):
    k = np.size(x, axis=0)
    x_moy = np.zeros((int(k/2), 2))
    y = np.zeros((int(k/2), 2))
    for i in range(int(k/2)):
        x_moy[i] = (-x[int(np.mod((2*i-2), k))] + 3 *
                    x[int(np.mod((2*i-1), k))] + 3*x[2*i] - x[2*i+1]) / 4
        y[i] = (x[int(np.mod((2*i-2), k))] - 3 *
                x[int(np.mod((2*i-1), k))] + 3*x[2*i] - x[2*i+1]) / 4
    return x_moy, y

def decompose_totale(x,y,n):
    if n != 0 :
        x1,y1 = decompose(x)
        new_y = np.concatenate((y1,y))
        return decompose_totale(x1,new_y,n-1)
    else :
        return x,y

def recompose(x,y):
    k = np.size(x, 2) * 2
    x_moy = np.zeros((int(k), 2))
    for i in range(int(k)):
        x_moy[np.mod(2*i,k)] = (3/4) * (x[i] + y[i]) + (1/4) * (x[i+1] - y[i+1])
        x_moy[np.mod(1+(2*i),k)] = (1/4) * (x[i] + y[i]) + (3/4) * (x[i+1] - y[i+1])
    return x_moy,y


def affichage(tab):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.add_patch(Polygon(tab[:len(tab),:], fill=False, closed= True))
    plt.axis([0, 15, 0, 15])
    plt.show()

def main() :
    herisson = np.loadtxt("herisson512.d")
    x1, y1 = decompose(herisson)
    # x4 = recompose(x1,y1)
    # affichage(x4)
    x2, y2 = decompose(x1)
    x3, y3 = decompose(x2)
    affichage(herisson)
    affichage(x1)
    affichage(x2)
    affichage(x3)
    decomp_a_afficher, yk = decompose_totale(herisson, herisson[0:0] ,1)
    affichage(decomp_a_afficher)
    # x4 = recompose(x1,y1)

main()