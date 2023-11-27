from matplotlib import pyplot as plt
import numpy as np
from numpy import exp
from typing import Callable, Tuple, List

EPSILON = 10 ** -5
ITERATION_MAX = 1000
N=10
    
# Points d'observations (ti, vi)
DATA1 = [(2, 2), (4, 4.3), (5, 4.9)]
DATA2 = [(1, 0.5), (2, 1), (3, 1.5),(4, 2), (5, 2.5), (6, 3)]





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
    
