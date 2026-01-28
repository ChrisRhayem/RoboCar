from affichage_terminal import avancer, reculer
from robocar import * 
from tkinter import *
from tkinter import ttk

def affiche(matrice:list, voiture:RoboCar, frm)->None:
    for i in range(len(matrice)):
        for j in range(len(matrice[i])-1):
            if (i, j) == voiture.coo:
                ttk.Label(frm, text=voiture.orientation()).grid(column=i, row=j)
            else:
                ttk.Label(frm, text=matrice[i][j]).grid(column=i, row=j)
        if (i, j+1) == voiture.coo:
            ttk.Label(frm, text=voiture.orientation()).grid(column=i, row=j+1)
        else:
            ttk.Label(frm, text=matrice[i][j+1]).grid(column=i, row=j+1)
    ttk.Label(frm, text=f"Coordoonées de la voiture: {voiture.coo}").grid(column=i+1, row=0)
    ttk.Label(frm, text=f"Orientation de la voiture: {voiture.orientation()}").grid(column=i+1, row=1)

def keypressed2(k):
    """
    Appel une fonction pour chaque touche pressé dans le terminale
    """
    if k.keysym == "Left":
        flash.s += -1
    if k.keysym == "Right":
        flash.s += 1
    if k.keysym == "Up":
        avancer(matrice, flash)
    if k.keysym == "Down":
        reculer(matrice, flash)
    affiche(matrice, flash, frm)

root = Tk()
root.bind('<KeyPress>', keypressed2)


flash = RoboCar("Flash", (1,1), 0, 0)
matrice = [["O" for _ in range(3)] for _ in range(3)]

frm = ttk.Frame(root, padding=10)
frm.grid()

affiche(matrice, flash, frm)

# ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
root.mainloop()