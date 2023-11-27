from matplotlib import pyplot as plt
import numpy as np
from numpy import exp

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