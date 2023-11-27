from  outils import *

# régression linéaire : y = a * t + b
# La fonction que nous voulons dériver est par rapport à a et b
def jacobienne(t) :
    # N est la longueur du vecteur t
    N = len(t)
    
    # Initialisation de la matrice Jacobienne avec des zéros
    jacobien = np.zeros((N, 2))  # 2 colonnes pour les dérivées par rapport à a et b
    
    # Calcul des dérivées partielles par rapport à a et b
    for i in range(N):
        jacobien[i, 0] = -t[i]  # Dérivée partielle par rapport à a
        jacobien[i, 1] = -1.0   # Dérivée partielle par rapport à b
    
    return jacobien


def fonctionCoutRegressionLineaire(a, b, t, v):
    """Calcule la fonction de coût de la régression linéaire.

    Args:
        a: Coefficient directeur de la droite.
        b: Ordonné à l'origine de la droite.
        t: Vecteur des abscisses des points d'observations.
        v: Vecteur des ordonnées des points d'observations.

    Returns:
        La fonction de coût.
    """

    return np.sum((v - (a * t + b)) ** 2)

def moindresCarre(t, v):
    """Calcule la droite d'ajustement linéaire des points d'observations.

    Args:
        t: Vecteur des abscisses des points d'observations.
        v: Vecteur des ordonnées des points d'observations.

    Returns:
        Le coefficient directeur et l'ordonnée à l'origine de la droite.
    """
    
    # Initialisation des paramètres
    a = 0
    b = 0

    # Calcul de la fonction de coût
    J = fonctionCoutRegressionLineaire(a, b, t, v)

    # Itération sur les paramètres jusqu'à convergence
    while True:
        # Mise à jour des paramètres
        a_new = (np.sum(t * (v - b)) / np.sum(t ** 2))
        b_new = np.mean(v - a_new * t)

        # Calcul de la nouvelle fonction de coût
        J_new = fonctionCoutRegressionLineaire(a_new, b_new, t, v)

        # Condition d'arrêt
        if np.abs(J - J_new) < EPSILON:
            break

        # Mise à jour des paramètres
        a = a_new
        b = b_new
        J = J_new

    return a, b


