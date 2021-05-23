#! usr/bin/python

#########################    PROJET PYTHON    ####################################################################
# AUTEURS DU PROJET : RUGERO CARL GAUSS ET YASSINE OUAKILI                                                       #
# DATE DE CREATION : 26 MARS 2021                                                                                #
# VERSION : V1                                                                                                   #
#                                                                                                                #
# NOM DU PROJET : SPACE INVADERS                                                                                 #
# NOM DU PROFESSEUR : CATHERINE DEZAN                                                                            #
##################################################################################################################


##################################     LES DIFFERENTS IMPORTS DU PROGRAMME    #################################### 

import tkinter as tk
import random as rd
from tkinter import *

from winsound import *
# Impport de la bibliothèque audio

##################################################################################################################

###################################               DEBUT DU PROGRAMME            ##################################

# La classe Defender qui permet de tirer sur des Aliens 

class Defender(object):
    def __init__(self): 
        self.width = 130
        self.height = 130
        self.move_delta = 20 
        self.id = None 
        self.player = PhotoImage(file="player6.png")
        self.max_fired_bullets = 8
        self.fired_bullets = []
        self.canvas_height = Fleet().get_height()
        self.canvas_width = Fleet().get_width()
        self.xi = self.canvas_width//2 - self.width//2
        self.yi = self.canvas_height*1.09 - self.height
        self.vie=3

# Les accesseurs permettent de mettre les coordonnées du Defender à jour

    def get_id(self):
        return self.id
    def get_firedB(self):
        return self.fired_bullets
    def get_xi(self):
        return self.xi
    def get_yi(self):
        return self.yi

    def set_firedB(self,liste):
        self.fired_bullets=liste
    def set_xi(self,newx):
        self.xi=newx
    def set_yi(self,newy):
        self.yi=newy

    # Méthode de positionnement de l'objet Defender  
    def install_in(self, canvas):
        self.canvas=canvas
        xi , yi = self.get_xi() , self.get_yi()
        w = self.width
        self.defender_object = canvas.create_image(xi+w//2 , yi,  image=self.player)

    # Méthode pour bouger le Defender en utilisant le clavier    
    def keypress(self, event):

        x_limit=self.get_xi()  # Rester dans le cadre du jeu horizontalement
        
        if event.keysym == 'Left': # Si on appuie sur la touche flèche Gauche
            if x_limit > 0:   

            # Positionnement et déplacement du Defender vers la Gauche
                self.set_xi(self.get_xi()-self.move_delta)     
                self.move_in(self.canvas,-self.move_delta)
                
        elif event.keysym == 'Right': # Si on appuie sur la touche flèche Droite
            if x_limit+self.move_delta < 0.9*self.canvas_width: 

            # Positionnement et déplacement du Defender vers la Droite 
                self.set_xi(self.get_xi()+self.move_delta)   
                self.move_in(self.canvas,self.move_delta)
                
        elif event.keysym == 'space':  # Si on appuie sur la touche flèche Espace

            # Les coordonnées du Defender changent en meme temps avec celles du Bullet, ainsi le Defender tire des bullets
            self.id = 1
            self.bullet = Bullet(self.id)
            self.bullet.set_x(self.get_xi())
            self.bullet.set_y(self.get_yi())
            self.fire(self.canvas)
        
    # Méthode pour déplacer horizontalement le Defender
    def move_in(self , canvas , dx):
        canvas.move(self.defender_object, dx, 0)
    
    # Méthode pour vérifier les tirs du Defender
    def fire(self, canvas):
        if len(self.fired_bullets) < self.max_fired_bullets: # Condition qui vérifie si le nombre de bullets est respecté
            self.bullet.id = self.bullet.install_in(self.canvas)    
            self.fired_bullets.append(self.bullet.id)    

    # Méthode qui gère les bullets (Déplacement, Tirs et Limite des bullets)       
    def move_bullet(self,canvas):
        for i in range(0,len(self.fired_bullets)):
            x,y,x1,y1 = self.canvas.bbox(self.fired_bullets[i]) # Mémorisation des coordonnées verticales du Bullet
            
            if y<0:    # Si le bullet est en dehors du cadre du jeu
                canvas.delete(self.fired_bullets[i])   #Le supprimer du jeu
                del self.fired_bullets[i]   # Le supprimer de la liste des bullets
                break

            else: # Sinon, les bullets continuent à se générer et à bouger
                self.bullet.move_in(self.canvas,self.fired_bullets[i])                      
    
    # Méthode de touche du Defender qui gère la collision du Bullet sur le Defender
    def defender_touched_by(self,canvas,fleet):
        res=False

        if len(fleet.aliens_fleet)>0:    
            x,y,x1,y1= self.canvas.bbox(self.defender_object) # Mémorisation des coordonnées du Defender
            collapsed = canvas.find_overlapping(x,y,x1,y1) # La liste collapsed recoit tout les bullets en collision avec le Defender

            for i in range(0,len(collapsed)): 
                for j in range(0,len(fleet.fired_bullet)):
                    if collapsed[i]==fleet.fired_bullet[j]:    # Si le bullet touche le Defender 
                        self.vie-=1                             # Le Defender perd une vie 
                        self.canvas.delete(fleet.fired_bullet[j]) # Supprimer le bullet du jeu
                        del fleet.fired_bullet[j]
                        print(self.vie)
                        res=True
                        break
                    
                if res == True:
                    break

#  La classe Fleet permet de regrouper un groupe d'aliens pour tirer sur le Defender

class Fleet(object):
    def __init__(self):
        self.aliens_lines = 4
        self.aliens_columns = 7
        self.aliens_inner_gap = 20
        self.alien_x_delta = 5
        self.alien_y_delta = 15
        fleet_size = self.aliens_lines * self.aliens_columns
        self.aliens_fleet = [None] * fleet_size
        self.width = 1000
        self.height = 800
        
        self.max_fired_bullets = 1
        self.fired_bullet=[]
        
        
   # Les accesseurs qui définissent l'espacement entre les Aliens
    def get_dx(self):
        return self.alien_x_delta
    def get_dy(self):
        return self.alien_y_delta
    def set_dx(self,new_dx):
        self.alien_x_delta=new_dx

    # Les accesseurs qui définissent la Largeur et la Longueur de l'objet Fleet  
    def get_width(self):
        return self.width
    def get_height(self):
        return self.height

# Méthode de positionnement de l'objet Fleet    
    def install_in(self, canvas):
        self.canvas=canvas
        self.alien=Alien()

        #Les coordonnées du positionnement de l'objet Fleet
        self.x=50  
        self.y=120

        move=0 

        # Création de la matrice d'Aliens 
        for i in range(0,self.aliens_lines):
            for j in range(0,self.aliens_columns):
                self.aliens_fleet[move] = self.alien.install_in(self.canvas,self.x,self.y)
                move+=1
                self.x += self.aliens_inner_gap+60  # La Largeur d'un alien
            self.x=50
            self.y += self.aliens_inner_gap+40   # La Longueur d'un alien

        self.x = 500

# Méthode pour faire bouger l'objet Fleet   
    def move_in(self, canvas): 
        if len(self.aliens_fleet)!=0:
            bunch_aliens = self.canvas.find_withtag("alien")
            x,y,x1,y1 = self.canvas.bbox("alien")

            if x1>=self.width: # Si Dépassement vers coté droit

                self.set_dx(-self.get_dx()) # Revenir vers le coté gauche
                dy=self.alien_y_delta   

            elif x<=0: # Si Dépassement vers coté gauche

                self.set_dx(-self.get_dx()) # Revenir vers le coté droit
                dy=self.alien_y_delta

            elif y1>=self.height-120: # Si le Fleet dépasse le Defender, c'est Game Over !
                
                self.canvas.delete(ALL)# suppression de tout le contenu du canvas
                #self.canvas.create_text(self.get_width()//2,self.get_height()//2,text="GAME OVER !",fill="RED",font="ARIAL 40") # Afficher le message Game over !
                self.game_over = PhotoImage(file='game_over2.gif')
                self.canvas.create_image(500,400,image=self.game_over)
            else: # Dépassement vers le milieu
                dy=0

            for i in range(0,len(bunch_aliens)):

                self.alien.move_in(self.canvas,bunch_aliens[i],2*self.alien_x_delta,dy) # Vitesse au niveau du déplacement horizontal
    
    # Méthode de positionnement des bullets des aliens
    def install_alien_bullet(self,canvas):
        
        if len(self.aliens_fleet)!=0:
            rand=rd.randint(0,len(self.aliens_fleet)-1) # Définition de la bibliothèque aléatoire
            alienx1,alieny1,alienx2,alieny2=self.canvas.bbox(self.aliens_fleet[rand])  # Définition des coordonnées de positionnement du bullet en aléatoire 
            self.id =1
            self.bullet = Bullet(self.id)
            self.bullet.set_x(alienx1)
            self.bullet.set_y(alieny2)
            self.fire(self.canvas)

    # Méthode de configuration des bullets
    def fire(self, canvas):
            if len(self.fired_bullet) < self.max_fired_bullets: # Si le bullet est tiré, recharger un nouveau bullet au niveau des aliens

                self.bullet.id = self.bullet.install_in(self.canvas) # Ajouter des bullets
                self.fired_bullet.append(self.bullet.id)# Ajouter le bullet tiré dans la liste fired_bullets

    # Méthode de déplacement du bullet
    def move_bullet(self,canvas):
        if len(self.fired_bullet)>0:
            for i in range(0,len(self.fired_bullet)):

                x,y,x1,y1 = self.canvas.bbox(self.fired_bullet[i])
                if y>self.height:    #si le bullet dépasse le cadre du jeu
                    canvas.delete(self.fired_bullet[i]) # Supprimer le bullet du canvas
                    del self.fired_bullet[i] # Le supprimer de la liste fired_bullet 
                    break
                else:
                    self.bullet.move_in_aliens(self.canvas,self.fired_bullet[i]) # Le bullet continue de se déplacer
    
    # Méthode de gestion des collisions avec les bullets du Defender       
    def manage_touched_aliens_by(self,canvas,defender):
        self.canvas=canvas
        self.defender=defender
        
        for i in range(len(self.defender.fired_bullets)):
            output=0   
            xbd,ybd,xbd1,ybd1=self.canvas.bbox(self.defender.fired_bullets[i]) # Définition des coordonnées des Bullets du Defender
            for j in range(len(self.aliens_fleet)):
                
                if self.aliens_fleet[j] != None: # S'il existe encore des Aliens dans le Fleet
                    xba,yba,xba1,yba1=self.canvas.bbox(self.aliens_fleet[j]) # Définition des coordonnées des Bullets des aliens (Fleet)
                    
                    if (xbd>=xba or xbd1>=xba) and (xbd<=xba1 or xbd1<=xba1) and ybd1<=yba1 and ybd1>=yba: # Condition pour savoir si le bullet a touché l'alien
                        self.alien.alien_touched_by(self.canvas,self.defender.fired_bullets[i])   # Gestion de la collision avec l'appel de la méthode alien_touched_by()
                        canvas.delete(self.defender.fired_bullets[i])      # Supprimer le bullet tiré du canvas
                        canvas.delete(self.aliens_fleet[j])    # Supprimer l'alien éliminé du canvas
                        self.alien.alive = False
                        del self.defender.fired_bullets[i]   # Supprimer le bullet du Defender de la liste fired_bullet
                        del self.aliens_fleet[j] # Supprimer l'alien de la matrice
                        output=1    # Après on sort de la boucle
                        break
                        
            if(output==1):
                break
    
# La classe AlienKing
class AlienKing(object):
    def __init__(self):
        self.id = None
        self.alive = True
        self.alien = PhotoImage(file="enemy.png")
        self.explosion = PhotoImage(file="explosion.gif")
    
    def install_in(self, canvas, x, y): 
        self.id = canvas.create_image(x, y, image=self.alien, tags="alien")
        return self.id


# La classe Alien représente un alien qui a pour objectif de tuer un Defender
    
class Alien(object):
    def __init__(self):
        self.id = None
        self.alive = True
        self.alien = PhotoImage(file="enemy.png")
        self.explosion = PhotoImage(file="explosion.gif")
   
# Méthode de positionnement de l'objet Alien     
    def install_in(self, canvas, x, y): 
        self.id = canvas.create_image(x, y, image=self.alien, tags="alien")
        return self.id

# Méthode pour faire bouger l'objet Alien 
    def move_in(self, canvas, alien, dx, dy):
        self.id=alien
        canvas.move(self.id, dx, dy)

# Méthode pour gérer la collision entre l'Alien et le bullet du Defender   
    def alien_touched_by(self,canvas,projectile):
        x,y,x1,y1=canvas.bbox(projectile)
        explosion = canvas.create_image(x+(x1-x)/2, y1+(y1-y)/2, image=self.explosion, tags="explosion")
        canvas.after(100,canvas.delete,explosion) 

# La classe Bullet représente les balles du Defender et des aliens qui s'entretuent

class Bullet(object):
    def __init__(self, shooter):

        self.width = 240
        self.radius = 10
        self.color = "red"
        self.speed = 10
        self.id = None
        self.shooter = shooter
        self.x=Defender().get_xi()
        self.y=Defender().get_yi()

# Les accesseurs pour mettre les coordonnées du Bullet à jour 
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def set_x(self,newx):
        self.x=newx
    def set_y(self,newy):
        self.y=newy

# Méthode qui permet le positionnement et l'alignement du Bullet avec le Defender
    def install_in(self, canvas):
        x=self.get_x() + 60
        y=self.get_y() - 5
        r=self.radius
        self.id = canvas.create_oval(x,y,x+r,y+r,fill="red") # Creation du bullet

        return self.id

# Méthode pour faire bouger le bullet du Defender   
    def move_in(self,canvas,ball):
        self.id=ball
        canvas.move(self.id, 0, -self.speed) # Déplacement Vertical des bullets du Bas vers le Haut : Il s'agit du Defender

# Méthode pour faire bouger le bullet des Aliens
    def move_in_aliens(self,canvas,ball):
        self.id=ball
        canvas.move(self.id, 0, self.speed) # Déplacement Vertical des bullets du Haut vers le Bas : Il s'agit des Aliens

# La classe Shield représente une barrière de protection qui se trouve devant l'objet Defender

class Shield(object):
    def __init__(self):
        self.protection=None
        self.width = 120
        self.life=3
        self.height = 80

    # Méthode de création d'un shield
    def install_in(self,canvas,x,y):
        self.canvas=canvas
        shield_creation=[(x,y),(x,y+3*self.height//4),(x+self.width//5,y+3*self.height//4),(x+self.width//5,y+2*self.height//4),(x+2*self.width//5,y+self.height//4),(x+3*self.width//5,y+self.height//4),(x+4*self.width//5,y+2*self.height//4),(x+4*self.width//5,y+3*self.height//4),(x+self.width,y+3*self.height//4),(x+self.width,y),(x+4*self.width//5,y-self.height//4),(x+self.width//5,y-self.height//4),(x,y)]
        # Création des différents points qui constituent une barrière de protection

        self.protection=self.canvas.create_polygon(shield_creation,fill="white",outline="black") # Matérialisation de ces points sous une forme de polygone en utilisant une méthode spécifique
        return self.protection

# La classe multiple_shields multiplie les shields en horizontal

class multiple_shields(object):
    def __init__(self):
        self.number=5 # Nombre de Shields dans la Canvas pour protéger l'objet Defender
        self.list_shields=[None]*self.number

    # Méthode de mutliplication des shields
    def install_in(self,canvas,x,y):
        self.canvas=canvas
        self.Shield=Shield() # Appel d'un shield dans le canvas

        for i in range(self.number): # Boucle de multiplication des shields
            self.list_shields[i]=self.Shield.install_in(self.canvas,x,y)
            x+=self.Shield.width*1.5
            #y-=self.Shield.width*1.5

    # Méthode qui permet de controler la collision d'un bullet sur un shield       
    def shield_touched(self,canvas,fleet):
        res=False
        res1=False

        if len(fleet.aliens_fleet)>0:

            for k in range(len(self.list_shields)):

                x,y,x1,y1= self.canvas.bbox(self.list_shields[k]) # Mémorisation des coordonnées d'un shield
                list = canvas.find_overlapping(x,y, x1, y1) # La liste 'list' recoit tout les bullets en collision avec le Shield

                for i in range(len(list)):
                    for j in range(len(fleet.fired_bullet)):

                        if list[i]==fleet.fired_bullet[j]: # Si le Bullet touche le Shield
                            
                            canvas.delete(fleet.fired_bullet[j]) # Supprime le bullet en collision avec le shield du canvas
                            del fleet.fired_bullet[j] # Supprime l'élément d'indice j de la liste fired_bullet
                            
                            canvas.delete(self.list_shields[k]) # Supprime le Shield du canvas
                            del self.list_shields[k] # Supprime l'élément d'indice k de la list_shield

                            res=True
                            res1=True
                            break

                    if res==True:
                         break
                if res1==True:
                    break           

# La classe Game permet de faire les différents jeux de données

class Game(object):
    def __init__(self, frame):

        #Taille de la fenetre du jeu
        width=1000 
        height=800

        
        self.frame=frame
        self.canvas=tk.Canvas(self.frame,width=width, height=height,bg="Black")
        #self.player = PhotoImage(file="space.jpg")

        self.background=PhotoImage(file='galaxy.png')
        self.canvas.create_image(400,420,image=self.background)

        self.game_over = PhotoImage(file='game_over1.gif')
        self.youwon = PhotoImage(file='you_win.gif')

        self.canvas.pack(side="top", fill="both", expand=True)
        self.fleet = Fleet()
        self.multiple_shields=multiple_shields()
        self.defender = Defender()
        self.defender.install_in(self.canvas)
        self.fleet.install_in(self.canvas)
        self.multiple_shields.install_in(self.canvas,50,600)
        self.points = 0
        self.life = StringVar()
        self.score =StringVar()

    def start_animation(self):
        self.animation()
        self.display_score() # Afficher le score du jeu
        self.display_life() # Afficher la vie du Defender
        self.display_title() # Afficher le titre principal

        #self.carre = canvas.create_image(xi+w//2 , yi,  image=self.player)

    # Accesseur qui définit la valeur du Score
    def set_score(self,value):
        self.score=value
        
    # Méthode d'animation qui permet de configurer les points, le score et la vie du Defender
    def animation(self):
        self.points= self.fleet.aliens_lines * self.fleet.aliens_columns - len(self.fleet.aliens_fleet) # Les points dépendent du nombre d'aliens partis
        self.score.set("SCORE : " + str(self.points)) # Le score dépend du nombre d'aliens tués
        self.life.set("LIFE : " + str(self.defender.vie)) #La vie du Defender dépend du nombre de collision avec les bullets des aliens
        
        if len(self.fleet.aliens_fleet)>0 and self.defender.vie>0 : 
            # Si le nombre d'aliens du Fleet est supérieur à 0 et que le Défender soit toujours en vie 

            self.fleet.move_in(self.canvas) # Fleet continue d'avancer
            self.move_bullets() # Les bullets continuent d'etre tirés
            self.fleet.manage_touched_aliens_by(self.canvas,self.defender) # Si les aliens sont touchés par les bullets du Defender, les supprimer du canvas
            self.fleet.install_alien_bullet(self.canvas) # Les aliens continuent de charger en Bullets
            self.defender.defender_touched_by(self.canvas,self.fleet) # Si le Defender est touché par les bullets des Aliens, mise à jour de sa vie
            self.multiple_shields.shield_touched(self.canvas,self.fleet) # Si le Shield est touché par les bullets des Aliens, le supprimer du canvas
            self.canvas.after(30,self.animation)

        elif self.defender.vie==0: # Si le niveau de vie du Defender est égal à 0

            self.canvas.delete(ALL)# Supprimer tout le contenu du canvas
            #self.canvas.create_text(self.fleet.get_width()//2,self.fleet.get_height()//2,text="GAME OVER !",fill="RED",font="ARIAL 40") # Aficher le message Game over !
            self.canvas.create_image(500,400,image=self.game_over)

        elif len(self.fleet.aliens_fleet)==0: # Si le nombre d'Aliens du Fleet est nul

            self.canvas.delete(ALL) # Supprimer tout le contenu du canvas
            #self.canvas.create_text(self.fleet.get_width()//2,self.fleet.get_height()//2,text="CONGRATULATION YOU'VE WON !",fill="GREEN",font="ARIAL 25") # Afficher le message Congratulation you've won !
            self.canvas.create_image(500,400,image=self.youwon)

    # Méthode pour bouger les bullets du Defender et des Aliens       
    def move_bullets(self):
        self.defender.move_bullet(self.canvas)
        self.fleet.move_bullet(self.canvas)
   
    # Méthode de mise à jour de positionnement du Fleet
    def move_aliens_fleet(self):
        self.fleet.move_in(self.canvas)

    # Méthode d'affichage du Score
    def display_score(self):
        self.score =StringVar()
        scoreLabel=Label(self.canvas,textvariable=self.score, font="Arial", bg='black', fg = "White")
        self.score.set("SCORE : " + str(self.points))
        self.canvas.create_window(50, 25, window = scoreLabel)  # Création d'une petite fenetre pour le label Score  

    # Méthode d'affichage du niveau de vie
    def display_life(self):
        self.life =StringVar()
        lifeLabel=Label(self.canvas,textvariable=self.life, font="Arial", bg='Black', fg = "white")
        self.life.set("LIFE : " + str(self.defender.vie))
        self.canvas.create_window(950, 25, window = lifeLabel)  # Création d'une petite fenetre pour le label Life  

    # Méthode d'affichage du Titre du Jeu
    def display_title(self) :
        progName = Label(self.canvas, text="SPACE INVADERS", font="ARIAL", bg = "black", fg = "White")
        progName.pack()
        self.canvas.create_window(500, 25, window = progName)  # Création d'une petite fenetre pour le label progName  

# La classe SpaceInvaders est la classe principale qui permet la création de la fenetre principale et son exécution    

class SpaceInvaders(object): 

    """
        MAIN CLASS 
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SPACE INVADERS")
        width=1000
        height=800

        self.musique_menu = PlaySound("audio1.wav", SND_FILENAME | SND_ASYNC)
        self.frame=tk.Frame(self.root,width=width, height=height,bg="green")
        self.frame.pack()
        self.game = Game(self.frame)
       
    def play(self):    
        self.game.start_animation()
        self.root.bind("<Key>", self.game.defender.keypress)
        self.root.mainloop()    # Affichage de la Fenetre du Jeu 
        
jeu=SpaceInvaders()
jeu.play()



##################################             FIN DU PROGRAMME                       #############################################