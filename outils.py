from matplotlib import pyplot as plt
import numpy as np
from numpy import exp
from typing import Callable, Tuple, List
import random
import math

###############################CONSTANTE########################
EPSILON = 10 ** -5
ITERATION_MAX = 1000
ITERATION_MAX_TSP = 200
N=10

DATA1 = [(2, 2), (4, 4.3), (5, 4.9)]
DATA2 = [(1, 0.5), (2, 1), (3, 1.5),(4, 2), (5, 2.5), (6, 3)]

RANGE_P = 15
RANGE_X = 15

N_PARTICULE = 6
N_POPULATION = 10
SOLUTION_TSP=9
DISTANCES_VILLES =[[0,1,1,3,4,5,6,1,7],
                   [1,0,5,4,3,6,1,9,2],
                   [2,5,0,1,6,1,9,3,7],
                   [3,4,1,0,5,9,7,2,1],
                   [4,3,6,5,0,9,1,2,1],
                   [5,6,1,9,9,0,2,1,7],
                   [6,1,9,7,1,2,0,4,5],
                   [1,9,3,2,2,1,4,0,7],
                   [7,2,7,1,1,7,5,7,0]]

def f1(x: float) -> float:
    """
    Retourne la valeur de f(x) pour un x donné
    """
    return (x - 2) ** 2


def df1(x: float) -> float:
    """
    Retourne la valeur de f'(x) pour un x donné
    """
    return 2 * x - 4


def g1(x: float) -> float:
    """
    Retourne la valeur de g(x) pour un x donné
    """
    return -exp(-(x - 1) ** 2) * (x - 2) ** 2


def dg1(x: float) -> float:
    """
    Retourne la valeur de g'(x) pour un x donné
    """
    return 2 * (x - 2) * (x**2 - 3 * x + 1) * exp(-(x-1)**2)


def f2(x: float) -> float:
    """
    Retourne la valeur de f(x) pour un x donné
    """
    return ((x - 1) ** 2)*(x-8)**2

def f3(x: float) -> float:
    """
    Retourne la valeur de f(x) pour un x donné
    """
    return 4/39*(x-10)**2+4
    

def generatePoints(N):
    """
    Génère N points sur la droite y = 2x + 1.
    N: Nombre de points à générer.
    Retourne Un vecteur t et un vecteur v de taille N × 1.
    """

    # Génération des abscisses
    t = np.linspace(0, 20, N)

    # Génération des ordonnées
    v = 2 * t + 1
    # Ajout du bruit aléatoire
    k=2
    e = np.random.rand(N)*k
    v += e

    return t, v


def permutation(individu, idx_cities):
    """
    Introduit une permutation de l'ordre de visite de deux villes parmis les villes que visite un individu

    vect_individu: L'ordre de visite des ville d'un individu.
    dist_v: matrice de distance représentant le coût de déplacement entre chaque ville

    Returns: Un nouvel ordre de visite des ville par un individu, et un boolean pour savoir si le nouveau parcours est tabou
    """
    new_individu = individu.copy()
    city_1 = new_individu[idx_cities[0]]
    city_2 = new_individu[idx_cities[1]]

    new_individu[idx_cities[0]] = city_2
    new_individu[idx_cities[1]] = city_1

    return new_individu


def subtract(X1, X2):
    """
    Calcule la vitesse faisant passer de la position x à la position y.

    Args:
    X1: La première position.
    X2: La deuxième position.

    Returns:
    La vitesse pour passer de X1 à X2.
    """
    vitesse = []
    for idx2 in range(len(X2)):
        i = 0
        for idx1 in range(len(X1)):
            if X1[idx1] == X2[idx2] and idx1!=idx2:
                vitesse.append([X1[idx2], X1[idx1]])
                X1 = permutation(X1, [idx1, idx2])

    return vitesse

def multiply(k, V):
    """
    Multiplie une vitesse par un réel.
    k: Le réel.
    V: La vitesse.
    Returns : La vitesse résultante.
    """

    result = []

    # Cas 0 < k < 1
    if 0 < k < 1:
        k = math.floor(k * len(V))
        for i in range(k):
            result.append(V[i])
        
    # Cas k est un entier
    elif isinstance(k, int):
        result = V * k

    # Cas k > 1
    elif k > 1:
        part_int, part_real = math.modf(k)
        result = add(multiply(part_int, V) , multiply(part_real, V))

    # Cas k < 0
    else:
        k = -k
        result = multiply(k, V)

    return result


def add(X, V):
    """
    Additionne deux positions ou une position et une vitesse.
    X: La première position ou la position.
    V: La deuxième vitesse ou la vitesse.
    Returns: La position ou la vitesse résultante.
    """
    # Vérification de la validité des entrées    
    result = []
    if isinstance(X, list):
        # Addition de deux vitesses
        for x in X:
          if isinstance(x, list):
              for i in X:
                  result.append(i)
              for i in V:
                  result.append(i)
              return result
    
    # Permutation
    new_x = X.copy()
    for v in V:
        va=v[0]
        vb=v[1]
        idx_new_va = 0
        idx_new_vb = 0
        for i in range(len(X)):
            if new_x[i] == va:
                idx_new_va = i
            if new_x[i] == vb:   
                idx_new_vb = i
        if idx_new_va != idx_new_vb:
            new_x[idx_new_va] = vb
            new_x[idx_new_vb] = va

    return new_x


def findMissingValues(individu):
    """
    Trouve trouve les villes non visité par un individu

    Args:
        individu: La liste des ville parcouru.

    Returns:
        La liste dess villes non visité
    """

    element_manquant = [1,2,3,4,5,6,7,8]
    element_found = []
    for i in range(1,len(individu)-1,1):
        if individu[i] not in element_found:
            element_found.append(individu[i])
    missing_values = [x for x in element_manquant if x not in element_found]
    return missing_values

def findDuplicate(individu:list) -> dict:
    """
    Trouve les villes visité deux fois

    Args:
        individu: liste des villes parcouru par individu

    Returns:
        un dictionnaire ayant pour clé le numéro de la ville visité deux fois et en valeur les moments(indice) où la ville est visité
    """

    occurrences = {}
    resultats = {}
    for i, element in enumerate(individu):
        if element not in occurrences:
            occurrences[element] = [i]
        else:
            occurrences[element].append(i)
    occurrences.pop(0)
    
    for element, indices in occurrences.items():
        if len(indices) > 1:
            resultats[element] = indices
    return resultats



def affichageFonctionAndFonctionD (f:Callable, df:Callable, name_f:str, name_df:str, color_f:str="red", color_df:str="blue", start:int=-1, stop:int=6):
    """
    Affichage de f(x) en rouge, f'(x) en bleu
    """
    x = np.linspace(start=start, stop=stop)
    plt.plot(x, f(x), color=color_f)
    plt.plot(x, df(x), color=color_df)
    plt.legend([name_f, name_df])
    plt.grid()
    plt.title("Visualisation de "+name_f+" et de "+name_df)
    plt.show()

def affichageGradient(f:Callable, name_f:str, name_grad_f:str, historique_gradient:list, xlim_a : int=-1, xlim_b : int=6, ylim_a : int=-0.5, ylim_b : int=10, start:int=-1, stop:int=6) :
    """
    Affichage de f(x) en rouge et suivi de l'évolution du gradient en bleu
    """
    x = np.linspace(start=start, stop=stop)
    plt.plot(x, f(x), color="red")
    plt.xlim(xlim_a, xlim_b)
    plt.ylim(ylim_a, ylim_b)
    for pointXY in historique_gradient:
        plt.plot(pointXY[0], pointXY[1], marker="o", markeredgecolor="blue", markerfacecolor="black", scalex="auto")
    plt.grid()
    plt.title("Descente de gradient de "+name_f+" itération par itération")
    plt.legend([name_f, name_grad_f])
    plt.show()


def affichageObsEtDroite(t, v, a, b):
    """Affichages les points observés et de la droite d'approximation linéaire associé

    Args:
        a: Coefficient directeur de la droite.
        b: Ordonné à l'origine de la droite.
        t: Vecteur des abscisses des points d'observations.
        v: Vecteur des ordonnées des points d'observations.
    """
    plt.plot(t, v, "o")
    plt.title("Points observés et approximation linéaire d'équation "+str(a)+"*t + "+str(b))
    plt.plot(t, a * t + b, "r")
    plt.plot()
    plt.show()

def affichagePointObserves(t,v):
    """Affichages les points observés

    Args:
        t: Vecteur des abscisses des points d'observations.
        v: Vecteur des ordonnées des points d'observations.
    """
    plt.plot(t, v, "o")
    plt.title("Représentation des points observés")
    plt.show()
    


def plotPSOEvolution(f, pso_results, xlima=0, xlimb=10, ylima=-100, ylimb=500):
    """
    Trace la fonction f et l'évolution des solutions Pg et Pi (i = 1, ..., k) sur un graphe.

    Args:
        f: La fonction à tracer.
        pso_results: Les résultats de l'algorithme PSO.
    """

    # Tracer la fonction f

    xs = np.linspace(xlima, xlimb, 100)
    ys = f(xs)
    plt.plot(xs, ys, label="f(x)")


    # Tracer l'évolution de P1
    plt.plot(pso_results[2], pso_results[3], 'o', label="P1")

    # Tracer l'évolution de P2
    plt.plot(pso_results[4], pso_results[5], '*', label="P2")

    # Tracer l'évolution de P3
    plt.plot(pso_results[6], pso_results[7], 'x', label="P3")

    # Tracer l'évolution de Pg
    plt.plot(pso_results[0], pso_results[1], '+', label="Pg")

    plt.xlabel("Itération")
    plt.ylabel("Valeur de la fonction objectif")
    plt.xlim(xlima,xlimb)
    plt.ylim(ylima, ylimb)
    plt.legend()
    plt.show()


def plotResolvingTsp(tsp_x_villes):
    fPs = {}
    for i in tsp_x_villes[2]: 
        for j in range(len(i)):
            if j not in fPs.keys():
                fPs[j] = []
            fPs[j].append(i[j])

    plt.plot(range(tsp_x_villes[3]), tsp_x_villes[1], 'o', label="cout meilleur chemin")
    for key_fPs in fPs.keys():
        plt.plot(range(tsp_x_villes[3]), fPs[key_fPs], '+', label="cout chemin"+str(key_fPs))


    plt.xlabel("Itération")
    plt.ylabel("Évolution du coût du parcours de toute les villes")
    plt.legend(loc="upper right",  bbox_to_anchor=(1.5, 1))
    plt.show()

