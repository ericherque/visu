import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
import math

def decomposition(array) :
    x_array = []
    y_array = []
    size = len(array)

    for index in range(0, size):
        # x_i^n value
        value = 1/4 * ( (-array[((2*index)-2)%size] + 3*array[(2*index-1)%size] + 3*array[(2*index)%size] - array[((2*index)+1)%size] ))
        x_array.append([value[0],value[1]])

        # y_i^n value
        value = 1/4 * ( (array[((2*index)-2)%size] - 3*array[(2*index-1)%size] + 3*array[(2*index)%size] - array[((2*index)+1)%size] ))
        y_array.append([value[0],value[1]])


    res = np.concatenate([x_array, y_array])
    return res

def affichage(tab):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.add_patch(Polygon(tab[0:len(tab),:], fill=False, closed=True))
    plt.axis([0, 15, 0, 15])
    plt.show()



def deconcatenation_x_y(tab):
    size = len(tab)
    tab_res = []
    i = 0
    while i < size // 2 :
        x = tab[i]
        y = tab[size // 2 +i]
        i += 1
        tab_res.append([x,y])
    return tab_res

def main() :
    herisson = np.loadtxt("herisson512.d")
    decomp_herisson = decomposition(herisson)
    decomp_herisson2 = decomposition(decomp_herisson)
    decomp_herisson3 = decomposition(decomp_herisson2)
    np_decomp_herisson = np.array(decomp_herisson)
    affichage(herisson)
    affichage(decomp_herisson[0:len(decomp_herisson)//2])
    affichage(decomp_herisson2[0:len(decomp_herisson)//4])
    affichage(decomp_herisson3[0:len(decomp_herisson)//8])

main()