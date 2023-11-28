from outils import *

def costGenetique(vect_individu:list, dist_v:list)->int:
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


def selection(population:list, cost_population:list)->list:
    """
    tri les parcours de chaque individu et retourne les parcours les moins couteux en premier

    Args:
        population: La liste des solutions.
        cost_population: La liste des cout associé

    Returns:
        Une liste de solutions.
    """
    pop_copy = population.copy()
    cost_pop_copy = cost_population.copy()
    selected_pop = []
    while len(cost_pop_copy)>0:
        idx_i = 0
        min_i = cost_pop_copy[idx_i]
        for idx_p_c in range(len(cost_pop_copy)):
            if cost_pop_copy[idx_p_c]<= min_i:
                min_i = cost_pop_copy[idx_p_c]
                pop_to_add = pop_copy[idx_p_c]
                idx_i = idx_p_c
        selected_pop.append(pop_to_add)
        
        del pop_copy[idx_i]
        del cost_pop_copy[idx_i]


    return selected_pop

def crossover(population:list, distances_villes:list)->list:
    """
    Croise les meilleurs parcours deux à deux en la moitié du parcours pour générer un nouveau parcours

    Args:
        population: la liste des parcours de chaque individu

    Returns:
        Une liste des n parcours les moins couteuse
    """

    new_population = []
    cost_new_population = []
    N = 10
    for i in range(0, len(population), 2):
        solution1 = population[i]
        solution2 = population[i + 1]
        
        # point de croisement au milieu
        point_croisement = len(solution1) // 2

        # Creuse les deux solutions à partir du point de croisement.
        solution_crosee1 = [0] 
        solution_crosee2 = [0] 
        solution_crosee3 = [0] 
        solution_crosee4 = [0] 
        solution_crosee5 = [0] 
        solution_crosee6 = [0] 
        solution_crosee7 = [0] 
        solution_crosee8 = [0] 

        #villes du parrcours1
        for i in solution1[:point_croisement]:
            if i !=0:
                solution_crosee1.append(i)
                solution_crosee2.append(i)

        for i in solution1[point_croisement:]:
            if i !=0:
                solution_crosee3.append(i)
                solution_crosee4.append(i)

        for i in solution2[:point_croisement]:
            if i !=0:
                solution_crosee5.append(i)
                solution_crosee6.append(i)

        for i in solution2[point_croisement:]:
            if i !=0:
                solution_crosee7.append(i)
                solution_crosee8.append(i)

        #villes du parcours 2
        for i in solution2[:point_croisement]:
            if i !=0:
                solution_crosee1.append(i)
                solution_crosee3.append(i)

        for i in solution2[point_croisement:]:
            if i !=0:
                solution_crosee2.append(i)
                solution_crosee4.append(i)

        for i in solution1[:point_croisement]:
            if i !=0:
                solution_crosee5.append(i)
                solution_crosee7.append(i)

        for i in solution1[point_croisement:]:
            if i !=0:
                solution_crosee6.append(i)
                solution_crosee8.append(i)

        population_croisee =list()
        population_croisee.append(solution_crosee1)
        population_croisee.append(solution_crosee2)
        population_croisee.append(solution_crosee3)
        population_croisee.append(solution_crosee4)
        population_croisee.append(solution_crosee5)
        population_croisee.append(solution_crosee6)
        population_croisee.append(solution_crosee7)
        population_croisee.append(solution_crosee8)

        for p_c in population_croisee:
            p_c.append(0)


        idx = 0
        for individu in population_croisee:
            missing_values = findMissingValues(individu=individu)
            if missing_values !=[]: 
                doublons = findDuplicate(individu=individu)
                for missing_v in  missing_values:
                    doublons_to_delete = random.sample(doublons.keys(),1)[0]
                    if len(doublons[doublons_to_delete])>1:
                        idx_doublons_to_delete = random.sample(doublons[doublons_to_delete],1)[0]

                    else:
                        idx_doublons_to_delete = doublons[doublons_to_delete]
                    individu[idx_doublons_to_delete] = missing_v
                    
                    del doublons[doublons_to_delete]
                
            idx+=1

        for p_c in population_croisee:
            new_population.append(p_c)
            cost_new_population.append(costGenetique(vect_individu=p_c, dist_v=distances_villes))
    return selection(population=new_population, cost_population=cost_new_population)[:N]

def mutation(population):
    """
    Introduit une permutation dans deux des parcours réalisé par les individu de la population

    Args:
        population: La liste des parcours de chaque individu.

    Returns:
        Une liste des parcours de chaque individu.
    """
    idx_mutations = random.sample(range(len(population)),2)
    new_population = population.copy()
    #choix des deux parcours aléatoire
    for idx in idx_mutations:
        # Choisit deux villes aléatoires.
        idx_cities = random.sample(new_population[idx] ,2)
        while 0 in idx_cities:
            idx_cities = random.sample(new_population[idx] ,2)
        city_1 = new_population[idx][idx_cities[0]]
        city_2 = new_population[idx][idx_cities[1]]

        # Echange les deux villes.
        new_population[idx][idx_cities[0]] = city_2
        new_population[idx][idx_cities[1]] = city_1

    return new_population

def tspGenetique(f: Callable, distances, n_population, n_iterations):
    """
    Résout le problème du voyageur de commerce en utilisant un algorithme génétique.
    f: fonction de calcul du cout d'un parcours
    distances: Une matrice des distances entre les villes.
    n_population: Le nombre de population.
    n_iterations: Le nombre d'itérations maximal possible.
    Returns: La solution optimale.
    """

    # Initialisation de la population et du critère d'arret
    individus = []
    compteur_critere_arret=0
    critere_arret=20
    iteration = 0
    meilleur_generation = 0
    for i in range(n_population) :
      individus.append([0,0,0,0,0,0,0,0,0,0])

    for i in range(n_population):
      for j in range(len(distances)-1):
        ville = random.randint(1, 8)
        while ville in individus [i] :
          ville = random.randint(1, 8)
        individus[i][j+1] = ville
    
    #suivi des meilleurs individus
    f_ens_individus =[]
    f_ens_best_individu_g = []

    best_individu_g = individus[0]
    f_best_individu_g = f(vect_individu=best_individu_g, dist_v=distances)
    best_individu_courant = best_individu_g
    f_best_individu_courant = f_best_individu_g

    ens_best_individu_g =[]

    # Boucle d'optimisation génétique
    while iteration < n_iterations:
        cost_individus = list()
        #cost_mutation_individus = list()
        
        for individu in individus:
            f_individu = f(vect_individu=individu, dist_v=distances)
            cost_individus.append(f_individu)
        selected_individus = selection(population=individus, cost_population=cost_individus)
        #for s in selected_individus :
            #print(s)

        #maj meilleur parcours dans la population courante
        best_individu_courant = selected_individus[0]
        f_best_individu_courant = f(vect_individu=best_individu_courant, dist_v=distances)
        
        crossed_individus = crossover(population=selected_individus[:6], distances_villes=distances)
        #for c in crossed_individus:
        #    print(c)

        mutation_individus = mutation(population=crossed_individus)
        #for m in mutation_individus:
            #print(m)
        
        for individu in mutation_individus:
            f_m_individu = f(vect_individu=individu, dist_v=distances)
            #cost_mutation_individus.append(f_m_individu)
        
        #maj meilleur solution global
        if f_best_individu_courant < f_best_individu_g:
            best_individu_g = best_individu_courant
            f_best_individu_g = f_best_individu_courant
            compteur_critere_arret = 0
            meilleur_generation = iteration
        else :
            compteur_critere_arret+=1


        if compteur_critere_arret>=critere_arret:
            break
        individus = mutation_individus
        ens_best_individu_g.append(best_individu_g)
        f_ens_best_individu_g.append(f_best_individu_g)
        f_ens_individus.append(cost_individus)
        iteration+=1

  # Retour de la solution optimale
    return ens_best_individu_g, f_ens_best_individu_g, f_ens_individus, iteration, meilleur_generation
