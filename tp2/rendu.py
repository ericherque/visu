import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
import math

def decomposition(array, x_len) :
    x_array = []
    y_array = []
    size = len(array)

    for index in range(0, x_len):
        # x_i^n value
        value = 1/4 * ( (-array[((2*index)-2)%size] + 3*array[(2*index-1)%size] + 3*array[(2*index)%size] - array[((2*index)+1)%size] ))
        x_array.append([value[0],value[1]])

        # y_i^n value
        value = 1/4 * ( (array[((2*index)-2)%size] - 3*array[(2*index-1)%size] + 3*array[(2*index)%size] - array[((2*index)+1)%size] ))
        y_array.append([value[0],value[1]])

    if x_len != 256 :
        for y_value in array[2*x_len:len(array)]:
            y_array.append([y_value[0],y_value[1]])

    res = np.concatenate([x_array, y_array])
    return res


def recomposition(array) :
    x_array = np.array(array[0:len(array)//2])
    y_array = np.array(array[len(array)//2:len(array)])

    res = []
    i = 0
    while i<len(array):
        # x pair
        value = 3/4 * (x_array[i] - y_array[i]) + 1/4 * (x_array[i+1] - y_array[i+1])
        res.append([value[0], value[1]])
        
        i += 1

        # x impair
        value = 1/4 * (x_array[i] - y_array[i]) + 3/4 * (x_array[i+1] - y_array[i+1])
        res.append([value[0], value[1]])

        i += 1
    
    return value



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
    ## avg: 512
    herisson = np.loadtxt("herisson512.d")
    ## avg: 256
    decomp_herisson = decomposition(herisson, len(herisson)//2)
    ## avg: 128
    decomp_herisson2 = decomposition(decomp_herisson, len(decomp_herisson)//4)
    ## avg: 64
    decomp_herisson3 = decomposition(decomp_herisson2, len(decomp_herisson)//8)
    ## avg: 32
    decomp_herisson4 = decomposition(decomp_herisson3, len(decomp_herisson)//16)
    ## avg: 16
    decomp_herisson5 = decomposition(decomp_herisson4, len(decomp_herisson)//32)
    ## avg: 8
    decomp_herisson6 = decomposition(decomp_herisson5, len(decomp_herisson)//64)
    ## avg: 4
    decomp_herisson7 = decomposition(decomp_herisson6, len(decomp_herisson)//128)

    #np_decomp_herisson = np.array(decomp_herisson)
    
    affichage(decomp_herisson[0:(len(decomp_herisson)//2)])
    affichage(decomp_herisson2[0:(len(decomp_herisson)//4)])
    affichage(decomp_herisson3[0:(len(decomp_herisson)//8)])
    affichage(decomp_herisson4[0:(len(decomp_herisson)//16)])
    affichage(decomp_herisson5[0:(len(decomp_herisson)//32)])
    affichage(decomp_herisson6[0:(len(decomp_herisson)//64)])
    affichage(decomp_herisson7[0:(len(decomp_herisson)//128)])

   #recomp_herisson = recomposition(decomp_herisson2)
    #recomp_herisson2 = recomposition(recomp_herisson)
    #affichage(recomp_herisson2[0:(len(recomp_herisson2)//2)])
    #affichage(decomp_herisson3[0:len(decomp_herisson)//8])

main()