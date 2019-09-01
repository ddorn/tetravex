import tkinter

def decoder(y):
    y = y-1
    t = y // (h*l)
    y = y - t*(h*l)
    i = y//l
    j = y-l*i
    return (i, j, t)

#Lire l'instance
b = int(input())
h = int(input())
l = int(input())

tuiles = []
for i in range(h*l):
    tuile = list(map(int, input().split()))
    tuiles.append(tuile)

top = tkinter.Tk()
global largeur
largeur = 100
W, H = 3*l*largeur, h*largeur
C = tkinter.Canvas(top, bg="white", height=H, width=W)


global colors
marge = 0
colors = ["white", "gray", "blue", "cyan", "yellow", "orange", "red", "mint cream", "azure", "violet red", "white"]
nbCouleurs = 10

def PoseTuile(i, j, cnf, t):
    print(t)
    x = j * (largeur + marge * 2)
    y = i * (largeur + marge*2)
    points = [[x, y], [x + largeur, y], [x + largeur, y + largeur], [x, y + largeur]]
    centre = x + largeur / 2, y + largeur / 2
    coord = [[points[0], points[1], centre], #NORD 0
     [points[1], points[2], centre], #EST 1
    [points[2], points[3], centre], #SUD 2
     [points[3], points[0], centre]] #OUEST 3
    Tris = list()
    for i in range(0, 4):
        C.create_polygon(coord[i], fill=colors[cnf[i]], width = 2, outline = "black")
    (C.create_rectangle(x+largeur//3, y+largeur//3, x+(largeur*2)//3, y +(largeur*2)//3, fill="white"))
    C.create_text((x+largeur//2,y+largeur//2), font=("Purisa", 30), text = str(t))
        
for i in range(h):
    for j in range(l):
        t = i*l+j
        PoseTuile(i, j, tuiles[t], t)

res = input()
print(" !", res)
res = list(map(int, input().split()))

for x in res:
    if x > 0:
        i,j,t = decoder(x)
        
        PoseTuile(i, j+l+2, tuiles[t], t)
C.pack()
top.mainloop()
