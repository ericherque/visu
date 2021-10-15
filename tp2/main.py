import matplotlib.pyplot as plt
import numpy as np
import math


#np.loadtxt() 
#np.savetxt()
#np.mod(array, size)

## decomposition totale de chaikin
def decomposition(array) :
    x_array = np.array([])
    y_array = np.array([])
    size = len(array)

    for index in range(0, size):
        # x_i^n value
        value = 1/4 * ( (-array[((2*index)-2)%size] + 3*array[(2*index-1)%size] + 3*array[(2*index)%size] - array[((2*index)+1)%size] ))
        x_array = np.append(x_array, value)

        # y_i^n value
        value = 1/4 * ( (array[((2*index)-2)%size] - 3*array[(2*index-1)%size] + 3*array[(2*index)%size] - array[((2*index)+1)%size] ))
        y_array = np.append(y_array, value)

    res = np.concatenate([x_array, y_array])
    print(res)

## recomposition totale de chaikin
def recomposition(array) :
    x_array = np.array([])
    y_array = np.array([])
    size = len(array) - 1

    #for index in range(0, size):


    #res = 

def main() :
    herisson = np.loadtxt("herisson512.d")

    np_herisson = np.array(herisson)
    decomp_herisson = decomposition(np_herisson)

    plt.plot(herisson)
    plt.show()

main()