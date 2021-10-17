import numpy as np
import math


## decomposition totale de chaikin
def decomposition(array) :
    x_array = np.array([])
    y_array = np.array([])
    size = len(array) - 1

    for index in range(0, size):
        # x_i^n value
        value = 1/4 * (-array[(2*index)-2] + 3*array[2*index-1] + 3*array[(2*index)] - array[(2*index)+1])
        x_array = np.append(x_array, value)

        # y_i^n value
        value = 1/4 * (array[(2*index)-2] - 3*array[2*index-1] + 3*array[2*index] - array[(2*index)+1])
        y_array = np.append(y_array, value)

    res = np.concatenate([x_array, y_array])