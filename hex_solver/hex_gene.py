"generateur aléatoire : prendre les conditions et générer une grille complète et résolue"
import random

def generateur(h,l,c):
    c=c-1
    grille=[[[random.randint(0, c),random.randint(0, c),random.randint(0, c), \
    random.randint(0, c), random.randint(0, c), random.randint(0, c)] \
    for t in range(l)] for _ in range(h)]  #6 couleurs pour une tuile
    
    print(h)
    print(l)
    
    for i in range(h):
        for j in range(l):
            cond = [i-1 >= 0 and j+1 < l, j+1 < l, i+1 < h]
            for k in range(3):
                if cond[k]:
                    vi = i
                    vj = j

                    if k == 2:
                        vi += 1
                    else:
                        vj += 1
                    if k == 0:
                        vi -= 1
                    #print("!", i, j, vi, vj, k)
                    grille[i][j][k+3]=grille[vi][vj][k]
    
    
    flat_grille = [item for sublist in grille for item in sublist]
    random.shuffle(flat_grille)
    for l in flat_grille:
        print(*l)



generateur(5,5,6)
