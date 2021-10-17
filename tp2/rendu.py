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


def affichage(tab):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.add_patch(Polygon(tab[:len(tab),:], fill=False, closed= True))
    plt.axis([0, 15, 0, 15])
    plt.show()

def main() :
    herisson = np.loadtxt("herisson512.d")
    # decomp_herisson = decomposition(herisson)
    # decomp_herisson2 = decomposition(decomp_herisson)
    # decomp_herisson3 = decomposition(decomp_herisson2)
    # decomp_herisson4 = decomposition(decomp_herisson3)
    # decomp_herisson5 = decomposition(decomp_herisson4)
    # np_decomp_herisson = np.array(decomp_herisson)
    # affichage(herisson)
    # affichage(decomp_herisson[0:(len(decomp_herisson))//2])
    # affichage(decomp_herisson2[0:(len(decomp_herisson2))//4])
    # affichage(decomp_herisson3[0:(len(decomp_herisson3))//8])
    x1, y1 = decompose(herisson)
    x2, y2 = decompose(x1)
    x3, y3 = decompose(x2)
    affichage(herisson)
    affichage(x1)
    affichage(x2)
    affichage(x3)

main()