from outils import *

def costTabou(vect_individu:list, dist_v:list)->int:
    """
    Calcule le coût du parcours de toute les villes par individu
    vect_individu: Un individu
    dist_v : matrice de distance entre les villes pour calculer le cout de déplacement entre chaque ville
    Returns:Le coût de la particule.
    """
    c_distance = 0
    for idx_v_i in range(len(vect_individu)-1):
        idx_v_i2 = (idx_v_i+1) %len(dist_v)
        x = vect_individu[ idx_v_i ]
        y = vect_individu[ idx_v_i2 ]
        
        c_v1_v2 = dist_v[x][y]
        c_distance += c_v1_v2
    return c_distance

def permutation(individu, idx_cities, tabou):
    """
    Introduit une permutation de l'ordre de visite de deux villes parmis les villes que visite un individu

    vect_individu: L'ordre de visite des ville d'un individu.
    dist_v: matrice de distance représentant le coût de déplacement entre chaque ville

    Returns: Un nouvel ordre de visite des ville par un individu, et un boolean pour savoir si le nouveau parcours est tabou
    """
    new_individu = individu.copy()

    # Choisit deux villes aléatoires, en dehors de la ville de départ et d'arrivée
    idx_cities = random.sample(new_individu ,2)
    while 0 in idx_cities:
        idx_cities = random.sample(new_individu ,2)
    city_1 = new_individu[idx_cities[0]]
    city_2 = new_individu[idx_cities[1]]

    # Echange l'ordre de visite des deux villes dans le parcours global d'un individu.
    new_individu[idx_cities[0]] = city_2
    new_individu[idx_cities[1]] = city_1

    #On détermine si le nouveau parcours est tabou
    individu_tabou = False
    for ind in tabou:
        if individu == ind[0] :
            individu_tabou = True

    return new_individu, individu_tabou


def tspTabou(f: Callable, distances, n_iterations, temps_interdiction):
    """
    Résout le problème du voyageur de commerce en utilisant un algorithme génétique.
    f: fonction de calcul du cout d'un parcours
    distances: Une matrice des distances entre les villes.
    n_iterations: Le nombre d'itérations maximal possible.
    temps_interdiction: durée pendant laquelle on considère un parcours comme étant tabou
    Returns: La solution optimale.
    """

    # Création de la liste de tabous.
    tabou = []
    compteur_best_inchange=20
    compteur = 0
    # Initialisation du parcours aléatoire x0 et du meilleur parcours x_best
    x0 = [0,0,0,0,0,0,0,0,0,0]
    x_best = x0
    f_x_best =  f(vect_individu= x_best, dist_v=distances)
    f_x_bests = []
    f_x1s = []
    for i in range(len(distances)-1):
        ville = random.randint(1, 8)
        while ville in x0 :
            ville = random.randint(1, 8)
        x0[i+1] = ville


    iteration = 0
    # Boucle d'optimisation génétique
    while iteration < n_iterations:
        #maj liste du temps restants des parcours  dans la liste tabou si possible 
        if len(tabou)>0:
            for t in tabou :
                t[2]-=1
        # modification aléatoire par permutation de l'ordre deux visite de deux ville
        x1 = permutation(individu=x0, idx_cities=random.sample(x0 ,2), tabou=tabou)
        #on vérifie que le nouveau parcours n'est pas tabou
        if not x1[1] :
            # Calcul du cout du nouveau parcours
            f_x1 = f(vect_individu= x1[0], dist_v=distances)
            f_x_best =  f(vect_individu= x_best, dist_v=distances)
            # Acceptation ou rejet du nouveau parcours.
            if f_x1 < f_x_best:
                x_best = x1[0]
                compteur = 0

            # intégration du nouveau parcours dans la liste tabou
            tabou.append([x1[0], f_x1, temps_interdiction])
        
        #suppression des parcours dont le temps d'interdiction est dépassé
        x_suppressions_tabou = []
        for t in range(len(tabou)):
            if tabou[t][2] == 0:
                x_suppressions_tabou.append(t)        
        for x in x_suppressions_tabou:
            del tabou[x]
        
        
        #Arrêt de l'algo si on a trouvé le meilleur parcours possible
        if compteur>= compteur_best_inchange:
            break
        x0 = x1[0]
        f_x_bests.append(f_x_best)
        f_x1s.append(f_x1)
        compteur+=1
        iteration+=1
        

  # Retour de la solution optimale
    return x_best, f_x_bests, f_x1s,iteration
