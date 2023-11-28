from outils import *

def psoSurFonction(f : Callable, x1:int, x2:int, x3:int, rho:float, N:int):
    """
    f : La fonction à optimiser.
    epsilon : La précision souhaitée.
    x1, x2, x3 : Les positions initiales des trois particules.
    v1, v2, v3 : Les vitesses initiales des trois particules.
    P1, P2, P3 : Les meilleures solutions trouvées par chaque particule jusqu'à présent.
    Pm : La solution optimale initiale
    rho : Un paramètre de contrôle de l'inertie.
    b1 et b2 : Des paramètres de contrôle de l'apprentissage.
    N : Le nombre maximal d'itérations

    Retourne Pg la solution optimale finale
    """
    i=0
    p1,p2,p3,pm,pg=random.sample(range(RANGE_P), 5)
    v1 = 0
    v2 = 0
    v3 = 0

    while(i < N):
        b1=random.uniform(0, 1)
        b2=random.uniform(0, 1)
        #choix meilleur solution entre p1, p2, p3
        if f(p1) < f(p2) and f(p1) < f(p3) :
            pg = p1
        elif f(p2) < f(p1) and f(p2) < f(p3):
            pg = p2
        elif f(p3) < f(p1) and f(p3) < f(p2):
            pg = p3
        
        #maj vitesses
        v1 = rho * v1 + b1 * (p1 - x1) + b2 * (pg-x1)
        v2 = rho * v2 + b1 * (p2 - x2) + b2 * (pg-x2)
        v3 = rho * v3 + b1 * (p3 - x3) + b2 * (pg-x3)

        #maj positions acutelles
        x1 +=v1
        x2 +=v2
        x3 +=v3

        #maj meilleur solution chaque particule
        if f(x1) < f(p1):
            p1 = x1
        if f(x2) < f(p2):
            p2 = x2
        if f(x3) < f(p3):
            p3 = x3
        
        if abs(f(pg) - f(pm))< EPSILON :
            return pg
        pm=pg
        i+=1
        
    return pg



def psoSurFonctionAvecEvolution(f : Callable, x1:int, x2:int, x3:int, rho:float, N:int):
    """
    Execute l'algorithme PSO et retourne l'évolution des solutions Pg, P1, P2 et P3.
    
    f: La fonction à optimiser.
    epsilon: La précision souhaitée.
    x1, x2, x3: Les positions initiales des trois particules.
    v1, v2, v3: Les vitesses initiales des trois particules.
    P1, P2, P3: Les meilleures solutions trouvées par chaque particule jusqu'à présent.
    Pm: La solution optimale.
    rho: Un paramètre de contrôle de l'inertie.
    b1 et b2: Des paramètres de contrôle de l'apprentissage.
    N: Le nombre maximal d'itérations.

    Retourne une liste contenant les évolutions des solutions Pg, P1, P2, P3 et les valeurs fPg, fP1, fP2, fP3 associées.
    """
    i=0
    v1, v2, v3 = [0,0,0]
    #v2 = 0
    #v3 = 0
    p1,p2,p3,pm,pg=random.sample(range(RANGE_P), 5)
  
    Pgs = [pm]
    PIs1 = [p1]
    PIs2 = [p2]
    PIs3 = [p3]

    fPgs = [f(pm)]
    fPIs1 = [f(p1)]
    fPIs2 = [f(p2)]
    fPIs3 = [f(p3)]
    while(i < N):
        b1=random.uniform(0, 1)
        b2=random.uniform(0, 1)
        #choix meilleur solution entre p1, p2, p3
        if f(p1) < f(p2) and f(p1) < f(p3) :
            pg = p1
            Pgs.append(pg)
            fPgs.append(f(pg))
        elif f(p2) < f(p1) and f(p2) < f(p3):
            pg = p2
            Pgs.append(pg)
            fPgs.append(f(pg))
        elif f(p3) < f(p1) and f(p3) < f(p2):
            pg = p3
            Pgs.append(pg)
            fPgs.append(f(pg))
        
        #maj vitesses
        v1 = rho * v1 + b1 * (p1 - x1) + b2 * (pg-x1)
        v2 = rho * v2 + b1 * (p2 - x2) + b2 * (pg-x2)
        v3 = rho * v3 + b1 * (p3 - x3) + b2 * (pg-x3)

        #maj positions acutelles
        x1 +=v1
        x2 +=v2
        x3 +=v3

        #maj meilleur solution chaque particule
        if f(x1) < f(p1):
            P1 = x1
            PIs1.append(p1)
            fPIs1.append(f(p1))
        if f(p2) < f(p2):
            p2 = x2
            PIs2.append(p2)
            fPIs2.append(f(p2))
        if f(x3) < f(p3):
            p3 = x3
            PIs3.append(p3)
            fPIs3.append(f(p3))
        
        # Arret si la meilleure solution Pg est suffisamment proche de la solution optimale Pm
        if abs(f(pg) - f(pm))< EPSILON :
            break
        pm = pg
        i+=1
        
        
    return [Pgs, fPgs, PIs1, fPIs1, PIs2, fPIs2, PIs3, fPIs3]



def updateVitesse(rho, vk, b1, b2, pi, pg, xk):
    """
    Met à jour la position en fonction de la vitesse.
    rho: Un paramètre de contrôle de l'inertie.
    vk : vitesse de la particule k
    b1 et b2: Des paramètres de contrôle de l'apprentissage.
    pi : meilleur solution de la particule k
    pg : meilleur solution de l'essaim
    xk : position de la particule k

    Returns:La nouvelle position.
    """

    PiXk = subtract(pi,xk)
    PgXk = subtract(pg,xk)
    b1PiXk = multiply(b1, PiXk)
    b2PgXk = multiply(b2, PgXk)
    rhoVk = multiply(rho, vk)

    results = add(add(rhoVk, b1PiXk),b2PgXk)
    return results   

def updatePosition(X, V):
    """
    Met à jour la position en fonction de la vitesse.
    X: La position.
    V: La vitesse.

    Returns: La nouvelle position.
    """
    return add(X=X, V=V)

def costPso(x, dist_v):
    """
    Calcule le coût du parcours de toute les villes d'une particule.
    particule: Une particule.
    
    Returns:Le coût de la particule.
    """
    c_distance = 0
    for idx_v_i in range(len(x)-1):
        idx_v_i2 = (idx_v_i+1) %len(dist_v)
        #print(idx_v_i2, x[ idx_v_i2 ])
        d1 = x[ idx_v_i ]
        d2 = x[ idx_v_i2 ]
        
        c_v1_v2 = dist_v[d1][d2]
        c_distance += c_v1_v2
    return c_distance



def tspPso(f: Callable, distances, n_particules, n_iterations):
    """
    Résout le problème du voyageur de commerce en utilisant le PSO.
    f: fonction de calcul du cout d'un parcours
    rho: Un paramètre de contrôle de l'inertie.
    distances: Une matrice des distances entre les villes.
    n_particles: Le nombre de particules.
    n_iterations: Le nombre d'itérations maximal possible.

    Returns: La solution optimale.
    """

    # Initialisation des particules
    # Initialisation des particules
    Pks = []
    Xks = []
    Vks = []
    ens_f_pg =[]
    ens_f_pks = []
    for i in range(n_particules):
      Pks.append([0,0,0,0,0,0,0,0,0,0])
      Xks.append([0,0,0,0,0,0,0,0,0,0])
      Vks.append([[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]])
      for j in range(len(distances)-1):
        ville = random.randint(1, 8)
        while ville in Xks[i] :
          ville = random.randint(1, 8)
        Xks[i][j+1] = ville
        Pks[i][j+1] = ville
    f_pks = [0 for _ in range(n_particules)]
    
    for i in range(n_particules):
      f_pks[i]=f(x=Pks[i], dist_v= distances)

    Pg0 = random.sample(Pks, 1)
    pg = Xks[0]
    f_pg = f(x=pg, dist_v= distances)
    rho = random.uniform(0,1)
    # Boucle d'optimisation
    iteration = 0
    compteur_best_inchange=20
    compteur = 0
    dernier_changement = 0
    while iteration < n_iterations:
        #b1 et b2: Des paramètres de contrôle de l'apprentissage.
        b1 = random.uniform(0,1)
        b2 = random.uniform(0,1)
        for idx in range(len(Pks)):
          if f_pks[idx] < f_pg:
            pg = Pks[idx]
            f_pg = f(x=Pks[idx], dist_v= distances)
            compteur = 0
            dernier_changement=iteration

        #Mise à jours des vitesses de chaque particules
        for j in range(len(Vks)):
            Vks[j] = updateVitesse(rho=rho, vk=Vks[j] , b1=b1
                                    , pi=Pks[j], xk=Xks[j], b2=b2, pg=pg)

        #Mise à jours positions
        for idx_xk in  range(len(Xks)):
          Xks[idx_xk] = updatePosition(Xks[idx_xk], Vks[idx_xk])

        #Mise à jours de la solution de chaque particule
        for idx_pk in  range(len(Pks)):
          f_xk = f(x=Xks[idx_pk], dist_v=distances)
          if f_xk< f_pks[idx_pk]:
            Pks[idx_pk] = Xks[idx_pk]
            f_pks[idx_pk] = f(x=Xks[idx_pk], dist_v=distances)
 
        #critere d'arret
        if compteur>= compteur_best_inchange:
          break
        Pg0=pg
        ens_f_pg.append(f_pg)
        ens_f_pks.append(f_pks)
        iteration+=1
        compteur+=1
    # Retour de la solution optimale
    return pg, ens_f_pg, ens_f_pks, iteration, dernier_changement
   