from  Outils import *

ALPHA = 0.01
ALPHA_MIN = 10**-6
ALPHA_MAX = 1.0


def gradient(fonctionfx: Callable, dfonctionfx: Callable, x0: float =0, precision_requise:float = EPSILON, iteration_max: int = ITERATION_MAX,
             alpha: float = ALPHA) -> Tuple[float, float, int]:
    """
    Retourne le min d'une fonction donné via l'algorithme du gradient
    fonctionfx: fonction f(x)
    dfonctionfx: f'(x)
    x0: the initial point of the function (x value)
    precision_requise: précision minimal pour stopper l'algorithme (ex: 10**-5)
    iteration_max: max number of iteration before stopping the algorithm. default = 1000
    alpha: pas après chaque itération (0.01 par défaut)
    retour: un tuple contenant la valeur min , le résultat f(x) et le nombre d'itération
    """
    dfx: float = dfonctionfx(x0)
    iteration: int = 0
    while abs(dfx) > precision_requise and iteration < iteration_max:
        dfx = dfonctionfx(x0)
        x0 = x0 - alpha * dfx
        iteration += 1
    return x0, fonctionfx(x0), iteration


def gradientAvecHistorique(fonctionfx: Callable, dfonctionfx: Callable, x0: float, precision_requise: float=EPSILON, iteration_max: int = ITERATION_MAX,
             alpha: float = ALPHA) -> Tuple[float, float, List[Tuple[float, float]]]:

    dfx: float = dfonctionfx(x0)
    iteration: int = 0
    liste_xys: List[List[float]] = [[x0, fonctionfx(x0)]]# Liste pour stocker les valeurs de x et f(x) correspondantes à chaque itération
    while abs(dfx) > precision_requise and iteration < iteration_max:
        dfx = dfonctionfx(x0)
        x0 = x0 - (alpha * dfx)
        iteration += 1
        liste_xys.append([x0, fonctionfx(x0)])


    return x0, fonctionfx(x0), liste_xys


def gradientAvecHistoriqueAlphaVariable(fonctionfx: Callable, dfonctionfx: Callable, x0: float, precision_requise: float, iteration_max: int = ITERATION_MAX,
             alpha: float = ALPHA, alpha_min: float = ALPHA_MIN, alpha_max: float = ALPHA_MAX) -> Tuple[float, float, List[Tuple[float, float]]]:

    dfx: float = dfonctionfx(x0)
    iteration: int = 0
    pas_alpha_a = 1.5
    pas_alpha_d=0.5
    liste_xys: List[List[float]] = [[x0, fonctionfx(x0)]]# Liste pour stocker les valeurs de x et f(x) correspondantes à chaque itération

    while abs(dfx) > precision_requise and iteration < iteration_max:
        dfx = dfonctionfx(x0)
        x1 = x0 - (alpha * dfx)
        
        # Vérifiez le signe de dfx(xn) et dfx(xn+1)
        signe_dfx_xn = 1 if dfx > 0 else -1 if dfx < 0 else 0
        signe_dfx_xn1 = 1 if dfonctionfx(x1) > 0 else -1 if dfonctionfx(x1) < 0 else 0
        
        if signe_dfx_xn == signe_dfx_xn1:
            # Les signes sont les mêmes, augmentez alpha
            alpha *= pas_alpha_a
        else:
            # Les signes sont différents, diminuez alpha
            alpha *= pas_alpha_d
        
        # Limitez alpha entre alpha_min et alpha_max
        alpha = max(alpha_min, min(alpha_max, alpha))

        x0 = x1
        iteration += 1
        liste_xys.append([x0, fonctionfx(x0)])

    return x0, fonctionfx(x0), liste_xys