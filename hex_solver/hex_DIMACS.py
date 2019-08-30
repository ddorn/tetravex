"""
Prend une grille hexagonale et affiche une formule booléenne en CNF

Mathinfoly 2019 - Romain Agéron
"""


def DIMACS_of_tetravex():
    h = int(input())
    l = int(input())
    nb_tuiles = h * l
    tuiles = [list(map(int, input().split())) for _ in range(nb_tuiles)]
    
    def trad_en_DIMACS(i, j, t):
        """Renvoie le numero de la variable booleene correspondant au 
        placement de la tuile t en (i,j)."""
        
        return t * nb_tuiles + (l * i + j) + 1
    
    incompatibles = [[[] for _ in range(nb_tuiles)] for _ in range(3)]
    
    for k in range(3):
        for t1 in range(nb_tuiles):
        	for t2 in range(nb_tuiles):
        		if t1 != t2:
        			if tuiles[t1][3+k] != tuiles[t2][k]:
        				incompatibles[k][t1].append(t2)
    
    
    print("p cnf ", nb_tuiles ** 2, " 42")
    
    
    for direc in range(3):
        # Contraintes d'adjacence (+1, 0)
        for i in range(h):
            for j in range(l):
                cond = [i-1 >= 0 and j+1 < l, j+1 < l, i+1 < h]
                if cond[direc]:
                    for t1 in range(nb_tuiles):
                        for t2 in incompatibles[direc][t1]:
                            vi = i
                            vj = j

                            if direc == 2:
                                vi += 1
                            else:
                                vj += 1
                            if direc == 0:
                                vi -= 1
                            print(-trad_en_DIMACS(i, j, t1), \
                                  -trad_en_DIMACS(vi, vj, t2), 0)


    # Surjectivite
    for pos in range(nb_tuiles):
        i, j = divmod(pos, l)
        for t in range(nb_tuiles):
            print(trad_en_DIMACS(i, j, t), end = " ")
        print(0)
    
    # Injectivite
    for pos in range(nb_tuiles):
        i, j = divmod(pos, l)
        for t1 in range(nb_tuiles):
            for t2 in range(t1):
                print(-trad_en_DIMACS(i, j, t1), -trad_en_DIMACS(i, j, t2), 0)
    
    # Toutes les tuiles sont utilisees
    for t in range(nb_tuiles):
        for pos in range(nb_tuiles):
            i, j = divmod(pos, l)
            print(trad_en_DIMACS(i, j, t), end = " ")
        print(0)
    
    
DIMACS_of_tetravex()
