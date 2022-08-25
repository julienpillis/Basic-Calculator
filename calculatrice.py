import math
from collections import deque
from tkinter import *
from math import *


class Fenetre(Tk):
    def __init__(self,h=482,l=352):
        Tk.__init__(self)                                           # On initialise la fênetre
        ecran_x = self.winfo_screenwidth()
        ecran_y = self.winfo_screenheight()
        fenetre_x = l
        fenetre_y = h
        pos_x = ecran_x // 2 - fenetre_x // 2                       # On la centre à l'écran
        pos_y = ecran_y // 2 - fenetre_y // 2
        geometrie = f"{fenetre_x}x{fenetre_y}+{pos_x}+{pos_y}"
        self.geometry(geometrie)
        self.config(bg="#101419")
        self.resizable(False,False)                                 # On fait en sorte qu'on ne puisse pas modifier la géométrie de la fenêtre

        self.__equationScreen = StringVar()                         # On définit l'équation que la fenêtre de calcul affichera
        self.__equationScreen.set("")
        self.__equationH = StringVar()                              # On définit l'équation que l'historique affichera
        self.__equationH.set("")
        self.__historique = deque()                                 # notre historique sera une file qui revient à sa forme initiale lorsque l'on sort de l'historique
        self.__indexHistorique=0

        self.__mode = StringVar()                                   # On définit le mode de calcul pour les fonctions trigonométriques (radians par défaut)
        self.__mode.set("RAD")


        self.title("TP Calculatrice")                               # On définit le titre de la fenêtre
        self.create_labels()
        self.create_buttons()


    def create_labels(self): # La fonction initialise et crée toutes les zones d'affichage

        self.__label_screen1 = Label(bg='#101419', textvariable=self.__equationH, fg='white', pady=(10),font=('Karla', 13),width=36,height=2,padx=12,relief='ridge')            # Etiquette de la zone d'affichage de l'historique
        self.__label_screen1.grid(columnspan=4)
        self.__label_screen2 = Label(bg='white',textvariable=self.__equationScreen,fg='black',font=('Karla',13),width=36,height=3,padx=12,relief='ridge')                       # Etiquette de la zone d'affichage du calcul
        self.__label_screen2.grid(columnspan=4)
        Label(self, textvariable=self.__mode, width=12, height=2,relief='ridge',pady=4, bg="#3e768e",fg="white").grid(row=11, column=2)                                         # Etiquette de la zone d'affichage du mode de calcul (radians ou degrés)


    def getHistorique(self):                            # La fonction permet d'afficher le premier élément de la file
        if(len(self.__historique)>0):                       # Si l'historique n'est pas vide, on peut l'afficher
            self.__equationH.set(self.__historique[0])      # On initialise la zone d'affiche comme le premier calcul de la file
            self.__historique.rotate(-1)                    # On décale les éléments de la pile vers la gauche (le premier, celui affiché, devient le dernier)
            self.__indexHistorique +=1                      # On mémorise le décalage
        else : self.__equationH.set('empty')


    def clearHistorique(self):                              # La fonction permet d'effacer la zone d'affichage de l'historique
        self.__historique.rotate(self.__indexHistorique)    # remise de l'historique à la dernière valeur calculée, on décale les éléments vers la droite
        self.__indexHistorique = 0                          # On remet le décalage à 0
        self.__equationH.set("")                            # On n'affiche rien

    def clear(self):
        self.__equationScreen.set("")

    def show(self, val):
        if("historique vide" in self.__equationH.get() ): self.clearHistorique()    # Si la zone historique affiche ce message, on remet la zone de l'historique à vide pour avoir un affichage propre
        if("=" in self.__equationScreen.get() ): self.clear()                       # Si la zone historique affiche ce message, on remet la zone de l'historique à vide pour avoir un affichage propre
        if(val=='π') : val = 'pi'                                                   # On transforme pi pour qu'elle soit compris par eval()
        if(val in ['sqrt','cos','sin','tan']) :
            if (val in ['cos', 'sin', 'tan']):                                      # si on fait appel à une fonction trigonométrique, on vérifie le mode de calcul
                if (self.__mode.get() == "DEG"):                                    # si le mode de calcul est en degré, il faut faire la conversion de la valeur entre parenthèses de radians à degrés
                    val =val+"(radians("
                if (self.__mode.get() == "RAD"):
                    val =val+"("
            else : val+='('
        self.__equationScreen.set((self.__equationScreen.get() + val)[:36])             # on fait attention à ne pas dépasser la taille du label

    def equal(self):                                                                    # Fonction associée à au bouton "="
        if ("=" in self.__equationScreen.get()): self.clear()                           # Si on a déjà effectué un calcul, on affiche une zone vide
        elif(self.__equationScreen.get()=="") : return                                  # Si la zone est vide, on ne fait rien
        else :
            try:
                eq= f"{self.__equationScreen.get()}\n={eval(self.__equationScreen.get())}"
                self.__equationScreen.set(eq[:40])                                 # On effectue l'opération à l'aide de la fonction eval() et on la convertit en chaîne de caractères
            except :
                eq = f"{self.__equationScreen.get()}\n=Error"
                self.__equationScreen.set(eq[:40])                                        # Si une erreur est rencontrée lors de l'opération, on l'indique
            finally :
                self.__historique.appendleft(self.__equationScreen.get())               # Mais dans tous les cas, on ajoute le résultat à la file


    def changeMode(self):                                                               # Fonction associée au bouton "DEG<->RAD"
        if(self.__mode.get()=="DEG") :                                                  # Si on appuie sur le bouton est qu'on est en mode "DEG", on passe en mode "RAD"
            self.__mode.set("RAD")
        else : self.__mode.set("DEG")                                                   # inversement

    def create_buttons(self):                                       # La fonction crée et initialise toutes les touches de la fenêtre
        buttons = ['1', '2', '3', '+', '4', '5', '6', '-', '7','8', '9', '*','0','.','π','**','(',')','tan','/','sin','sqrt','cos','=']
        column,row = 0,3                                             # On initialise les valeurs initiales pour placer les boutons sur la grille
        for button in buttons :                                      # Pour chaque bouton
            b = Button(self,text= button,command=lambda x=button :self.show(x),width=10,height=2,relief='ridge',padx=4,pady=-4) # On le crée
            b.grid(row=row,column=column)                                                                                       # On le place
            if column == 3: b.config(bg='#ffa500')                                                                              # S'il est en 3 ème colonne, on change de couleur car c'est un opérateur
            if button=="=": b.config(command=self.equal)                                                                        # Si le bouton est "=", on change sa fonction
            if column==3 :                                                                                                      # Si on atteint la colonne 3, on passe à la ligne du dessous et la colonne est donc 0
                column=0
                row+=1
            else :                                                                                                              # Sinon, on place le prochain bouton juste à droite
                column+=1
        Button(self, text='CLEAR', command=self.clear, width=49, height=2, relief='ridge',bg="#e60000").grid(columnspan=4,row=9)
        Button(self, text='PREV', command=self.getHistorique, width=20, height=2, padx=14,relief='ridge', bg="#ffa500").grid(row=10, columnspan=2)
        Button(self, text='CLEAR PREV', command=self.clearHistorique, width=20, height=2, padx=14,relief='ridge', bg="#ffa500").grid(row=10, column=2, columnspan=2)
        Button(self, text='DEG<->RAD', command=self.changeMode, width=20, height=2, padx=14, relief='ridge',bg="#ffa500").grid(row=11, column=0, columnspan=2)
        Button(self, text='EXIT',command=self.quit, width=11, height=2, fg='black', relief='ridge', pady=1,bg="#e60000").grid(row=11,column=3)


def main():
    calculatrice = Fenetre()
    calculatrice.mainloop()
if __name__ == '__main__':
    main()