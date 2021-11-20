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

def decompose_compression(x,e):
    n = 0
    k = np.size(x, axis=0)
    x_moy = np.zeros((int(k/2), 2))
    y = np.zeros((int(k/2), 2))
    for i in range(int(k/2)):
        x_moy[i] = (-x[int(np.mod((2*i-2), k))] + 3 *
                    x[int(np.mod((2*i-1), k))] + 3*x[2*i] - x[2*i+1]) / 4
        y_int = (x[int(np.mod((2*i-2), k))] - 3 *
                x[int(np.mod((2*i-1), k))] + 3*x[2*i] - x[2*i+1]) / 4
        if math.sqrt(math.pow(y_int[0],2) + math.pow(y_int[1],2)) < e :
            y[i] = np.array([0,0])
            n += 1
        else :
            y[i] = y_int
    return x_moy, y, n

def decompose_totale(x,y,n):
    if n != 0 :
        x1,y1 = decompose(x)
        new_y = np.concatenate((y1,y))
        return decompose_totale(x1,new_y,n-1)
    else :
        return x,y

def decompose_totale_compression(x,y,n,e,k):
    if n != 0 :
        x1,y1,k1 = decompose_compression(x,e)
        new_y = np.concatenate((y1,y))
        return decompose_totale_compression(x1,new_y,n-1,e,k+k1)
    else :
        return x,y,k

def recompose(x,y):
    k = np.size(x)
    x_moy = np.zeros((int(k), 2))
    tour = k//2
    i = 0
    while i < tour:
        x_moy[np.mod(2*i,k)] = (3/4) * (x[i] + y[i]) + (1/4) * ( x[np.mod(i+1,len(x))] - y[np.mod(i+1,len(y))] )
        x_moy[np.mod(1+(2*i),k)] = (1/4) * (x[i] + y[i]) + (3/4) * (x[np.mod(i+1,len(x))] - y[np.mod(i+1,len(y))])
        i += 1
    return x_moy,y[len(x):len(y)]

def recompose_totale(x,y):
    if np.size(y) == 0 :
        return x
    else :
        x1,y1 = recompose(x,y)
        print("taille de x1= ",np.size(x1)," taille de y1= ", np.size(y1))
        return recompose_totale(x1,y1)



def affichage(tab):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.add_patch(Polygon(tab[:len(tab),:], fill=False, closed= True))
    plt.axis([0, 15, 0, 15])
    plt.show()

def impression_erreur(tab, niv_decomp, epsilon_max, step) :
    i =0
    tab2 = []
    while i < epsilon_max :
        x, y, n= decompose_totale_compression(tab, tab[0:0],niv_decomp ,i,0)
        tab2.append([n,i])
        i += step
    for elem in tab2 :
        plt.plot(elem[1],elem[0],marker="o",color =  "red")
    plt.show()


def main() :
    herisson = np.loadtxt("herisson512.d")
    affichage(herisson)
    x1, y1 = decompose_totale(herisson, herisson[0:0] ,5)
    recomp_x1 = recompose_totale(x1, y1)
    affichage(x1)
    affichage(recomp_x1)
    crocodile = np.loadtxt("crocodile512.d")
    affichage(crocodile)
    x2, y2 = decompose_totale(crocodile, crocodile[0:0] ,1)
    affichage(x2)
    recomp_x2 = recompose_totale(x2,y2)
    affichage(recomp_x2)
    x3, y3, n3 = decompose_totale_compression(crocodile, crocodile[0:0] ,5,0.5,0)
    recomp_x3 = recompose_totale(x3,y3)
    affichage(recomp_x3)
    x4, y4, n4 = decompose_totale_compression(crocodile, crocodile[0:0] ,5,0.75,0)
    recomp_x4 = recompose_totale(x4,y4)
    affichage(recomp_x4)
    x5, y5, n5 = decompose_totale_compression(crocodile, crocodile[0:0] ,5,1.25,0)
    recomp_x5 = recompose_totale(x5,y5)
    affichage(recomp_x5)
    impression_erreur(crocodile,5,1.26,0.05)

main()