import matplotlib.pyplot as plt
import numpy as np
import math

import decomp_util as dcp
import recomp_util as rcp

#np.loadtxt() 
#np.savetxt()

def main() :
    herisson = np.loadtxt("herisson512.d")
    decomp_herisson = dcp.decompositon(herisson)
    plt.plot(herisson)
    plt.show()