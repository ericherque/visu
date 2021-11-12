import math
#Entree:
#   - une liste de points {X_1, ..., X_n} dans R^2
#   - une liste de valeurs {f_1, ..., f_n}
#   - les paramètres {µ_1, ..., µ_n}
#   - un point X
#
#Sortie:
#   > F(X)
#

def distance(x1,x2) :
    res = srqt(pow(x2[0]-x1[0],2)+pow(x2[1]-x1[1],2)+pow(x2[2]-x1[0],3))
    return res

def f_exemple(x,y) :
    return math.cos(x/2) * math.sin(x**2 + y)

def weight(x, y, x_tab, y_tab, u, ind) :
    N = len(x_tab)
    intermedia_a = 1
    k = 0
    while k != 0 :
        if(k != ind):
            intermedia_a = intermedia_a * pow(distance((x,y), (x_tab[k], y_tab[k])), u[ind])
        k += 1





print(f_exemple(0,2))

# def funcSheperd(x, y, u:
#     #TODO

