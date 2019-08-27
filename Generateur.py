"generateur aléatoire : prendre les conditions et générer une grille complète et résolue"
import random

def generateur(h,l,c):
    grille=[[0,0,0,0] for t in range (h*l)]  #4 couleurs pour une tuile
    c=c-1
    print(h,l)
    print(c+1)

    for i in range (h*l):
        colonne=i%l
        if l-1!= colonne :
            grille[i][1]=grille[i+1][3]=random.randint(0, c)
        else:
            grille[i][1]= random.randint(0, c)
        if colonne==0:
            grille[i][3] = random.randint(0, c)

    for i in range (h*l):
        if i < (h - 1) * l:
            grille[i][2] = grille[i + l][0] = random.randint(0, c)
        else:
            grille[i][2]  = random.randint(0, c)
        if i<l:
            grille[i][0] = random.randint(0, c)

    random.shuffle(grille)

    for t in grille:
        print(*t)



generateur(3,5,4)