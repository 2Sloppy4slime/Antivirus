

import pygame

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#On défini la grille:
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
class Grille():
    
    #   On représente la grille comme étant en diagonale pour une meilleure approche au mouvement
    #   chaque ligne diagonale est donc un "row" de nom et de taille différente:
    #
    #  exit
    #   4       3       2       1
    #       4       3       2
    #   5       4       3       2
    #       5       4       3   
    #   6       5       4       3
    #       6       5       4       
    #   7       6       5       4
    #
    #-----------------------------------------------------
    #pour représenter la position d'un point dans la grille, on utilise un tuple (row, pos) avec pos = l'index correspondant au point. donc (1,0) serait le coin en haut à gauche
    #-----------------------------------------------------

    
    def __init__(self) -> None:
        self.rows = {}
        self.rows["1"] =       [0]
        self.rows["2"] =     [0,0,0]
        self.rows["3"] =   [0,0,0,0,0]
        self.rows["4"] = [0,0,0,0,0,0,0] #voici comment on voit la grille
        self.rows["5"] =   [0,0,0,0,0] #chaque nombre représente l'état actuel de la case : 0 veut dire vide ; 1 veut dire bloqué par un mur et un autre nombre 
        self.rows["6"] =     [0,0,0] #un meilleur moyen serait de ne faire qu'une seule liste mais cela serait un peu plus confus, ici, tout est clair niveau mouvement
        self.rows["7"] =       [0]

        
        self.exit =[0]


    def stateOf(self,pos = (1,0)): #renvoie l'état de la position (0 est vide, 1 est un mur immobile, le reste est selon l'index de l'objet)
        if pos[1] < len(self.rows[str(pos[0])]) and pos[1] > -1 :
            return self.rows[str(pos[0])][pos[1]]
        else : raise IndexError("tried to reach out of bounds")

    def stateSet(self,index,pos = (1,0)) -> None : #Change l'état d'une position sur la grille, sera utilisé pour les murs + les mouvements
        if pos[1] < len(self.rows[str(pos[0])]) and pos[1] > -1 :
            self.rows[str(pos[0])][pos[1]] = index
        
    def reset(self) -> None :
        self.rows["1"] =       [0]
        self.rows["2"] =     [0,0,0]
        self.rows["3"] =   [0,0,0,0,0]
        self.rows["4"] = [0,0,0,0,0,0,0] 
        self.rows["5"] =   [0,0,0,0,0] 
        self.rows["6"] =     [0,0,0] 
        self.rows["7"] =       [0]
        self.exit[0] = 0


#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#On défini les pièces de base en dessous:
#---------------------------------------------------------------------------------------------------------------------------------------------------------------      
        


class Piece(): #Objet de base pour tout GameObject qui bouge

    def sortValues(self):
        self.points = sorted(self.points)


    def __init__(self,pos,index,surface: Grille) -> None:
        
        self.index = index
        self.points = [pos]
        self.sortValues() #inutile ici mais sert de modèle pour faire les autres
        for i in self.points:
            surface.stateSet(self.index,i)
        
    

    def mvtHorizontal(self,amount,surface : Grille, entitylist): #horizontal par rapport au losange au dessus donc dans ce sens là : "\" pour la grille graphique
        snd_moved = pygame.mixer.Sound("canmove.mp3")
        snd_stopped = pygame.mixer.Sound("cantmove.mp3")
        collision = False  
        collidedindex = 0
        for i in self.points :
                try:
                    test = surface.stateOf((i[0],i[1] + 1*amount))
                    if test > 1 and test != self.index :
                        collision = True
                        collidedindex = test
                        print("collided with : ", test)

                    if test == 0 or test == self.index:
                        pass
                    else: 
                        if collision == True and entitylist[collidedindex -2].checkMvtHorizontal(amount,surface,entitylist) == False:
                            raise IndexError("tried to move nowhere")
                          
                        if collision == False : 
                            raise IndexError("tried to move nowhere")
                        
                        
                    
                except : return
                
                else : pass

        
        if collision == True:
            print("yeag")
            entitylist[collidedindex -2].mvtHorizontal(amount,surface,entitylist)

        if amount > 0 : 
            self.points = sorted(self.points,reverse=True)



        it = 0
        for i in self.points : 
                if surface.stateOf((i[0],i[1] + 1*amount)) == 0:
                    self.points[it] = (i[0],i[1] + 1*amount)
                    surface.stateSet(self.index,(i[0],i[1] + 1*amount))
                    surface.stateSet(0,(i[0],i[1]))
                    it += 1
                else : 
                    it += 1
                    return 

        self.points = sorted(self.points)

    def checkMvtHorizontal(self,amount, surface : Grille,entitylist):
        for i in self.points :
                try:
                    test = surface.stateOf((i[0],i[1] + 1*amount))
                    if test == 0 or test == self.index:
                        pass
                    else:    
                        raise IndexError("tried to move nowhere")
                    
                except : return False
                
                else : pass
        return True


    def mvtVertical(self,amount,surface :Grille,entitylist): #vertical par rapport au losange au dessus donc dans ce sens là : "/" pour la grille graphique



        collision = False
        collidedindex = 0
        #on vérifie si le mouvement est possible
        for i in self.points:
            try:
                    
                    sens = 1 *amount
                    if i[0] > 4: 
                        sens = -1 *amount
                    elif i[0] == 4:
                        sens = -1
                    

                    test = i[1] +sens
                    
                    
                    if test < 0 :
                        print("invalide position checked")
                        raise IndexError("invalid conversion")                    
                    
                    test = surface.stateOf((i[0]+ 1*amount ,i[1] +sens))
                    if test > 1 and test != self.index :
                        collision = True
                        collidedindex = test
                        print("collided with : ", test)

                    if test == 0 or test == self.index:
                        
                        pass

                    else:    
                        if collision == True and entitylist[collidedindex -2].checkMvtVertical(amount,surface,entitylist) == False:
                            raise IndexError("tried to move nowhere")
                        if collision == False:
                            
                            raise IndexError("tried to move nowhere")
            except : 
                print("can't move" )
                return
                
            else : pass
        
        if collision:
            entitylist[collidedindex -2].mvtVertical(amount,surface,entitylist)

        #on trie dans le bon sens pour eviter de déplacer un point sur un autre de lui même
        if amount > 0 : 
            self.points = sorted(self.points,reverse=True)



        it = 0
        for i in self.points : 
                
                #on doit faire +1 sur l'index quand on est sur une ligne en dessous de 4 pour un mouvement correct
                sens = 1 * amount
                if i[0] > 4: 
                    sens = -1 * amount
                elif i[0] == 4:
                    sens = -1
                #on déplace tout les points sur la grille et dans l'objet
    
                if surface.stateOf((i[0] + 1*amount ,i[1] +sens )) == 0:
                    self.points[it] = (i[0] + 1*amount , i[1] +sens)
                    surface.stateSet(self.index,(i[0] + 1*amount , i[1] +sens))
                    surface.stateSet(0,(i[0],i[1]))
                    it += 1
                else : 
                    it += 1
                    return 

        self.points = sorted(self.points)
    
    def checkMvtVertical(self,amount,surface,entitylist):
        for i in self.points:
            try:
                    
                    sens = 1 *amount
                    if i[0] > 4: 
                        sens = -1 *amount
                    elif i[0] == 4:
                        sens = -1
                    test = i[1] +sens

                    if test < 0 :
                        print("invalide position checked")
                        raise IndexError("invalid conversion")                    
                    
                    test = surface.stateOf((i[0]+ 1*amount ,i[1] +sens))
                    if test == 0 or test == self.index:
                        
                        pass

                    else:    
                        
                        raise IndexError("tried to move nowhere")
                    
            except : return False
                
            else : pass

        return True






class Virus(Piece):
    def __init__(self,pos,surface : Grille) -> None: 
        Piece.__init__(self,pos,2,surface)
        self.points.append((pos[0],pos[1]+1)) #pas besoin de rotation
        self.sortValues()
        for i in self.points:
            surface.stateSet(self.index,i)



    def setPos(self,pos = (4,0)):
        self.points[0] = pos
        self.points[1] = (pos[0],pos[1]+1)
        
    def mvtHorizontal(self, amount, surface : Grille, entitylist): #on ne modifie que le mouvement horizontal car on a besoin de vérifier si on gagne
        if self.points[0] == (4,0) and amount < 0: # (4,0) est la position
            surface.exit[0] = 1 

            return
        else: 
            super().mvtHorizontal(amount, surface,entitylist)





#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#On défini les pièces de construction :
#---------------------------------------------------------------------------------------------------------------------------------------------------------------

# on a donc:
#
# ---- diagonale ----
# 
# schéma : 
#
#   0        0
#    0  ou  0
#

class Diagonale(Piece) :
    def __init__(self, pos, index, surface: Grille, reverse = False) -> None:
        super().__init__(pos, index, surface)
        if reverse == False: #Dans le même sens que le virus
            self.points.append((pos[0],pos[1]+1))
        else:
            if self.points[0][0] < 4:
                self.points.append((pos[0]+1,pos[1]+1))
            else: self.points.append((pos[0]+1,pos[1]-1))
        

        self.sortValues()
        for i in self.points:
            surface.stateSet(self.index,i)


#
# ---- verticale ----
# 
# schéma : 
#
#   0       
#   0


class Verticale(Piece):
    def __init__(self, pos, index, surface: Grille) -> None:
        super().__init__(pos, index, surface)
        if self.points[0][0] >= 4:
            self.points.append((self.points[0][0] +1 , self.points[0][1]))

        else:
            self.points.append((self.points[0][0] +1 , self.points[0][1] + 2))

        self.sortValues()
        for i in self.points:
            surface.stateSet(self.index,i)


#
# ---- horizontale ----
# 
# schéma : 
#
#   0 0     
#   

class Horizontale(Piece):
    def __init__(self, pos, index, surface: Grille) -> None:
        super().__init__(pos, index, surface)

        if self.points[0][0] > 4:
            self.points.append((self.points[0][0] -1 , self.points[0][1] + 2))
        
        else:
            self.points.append((self.points[0][0] -1 , self.points[0][1]))

        self.sortValues()
        for i in self.points:
            surface.stateSet(self.index,i)


#
# ---- Coin ----
# 
# schéma : 
#
#   0 0     ou      0 0
#     0             0


class Coin(Piece):
    def __init__(self, pos, index, surface: Grille,reverse = False) -> None:
        super().__init__(pos, index, surface)
        if reverse == False:
            if self.points[0][0] > 4:
                self.points.append((self.points[0][0]  , self.points[0][1] +2))
                self.points.append((self.points[0][0] -1 , self.points[0][1] + 2))
            
            else:
                self.points.append((self.points[0][0] -1 , self.points[0][1]))
                self.points.append((self.points[0][0] , self.points[0][1] + 2))
        else:
            if self.points[0][0] > 4:
                self.points.append((self.points[0][0] +1 , self.points[0][1] ))
                self.points.append((self.points[0][0] -1 , self.points[0][1] + 2))
            
            elif self.points[0][0] == 4:
                self.points.append((self.points[0][0] -1 , self.points[0][1]))
                self.points.append((self.points[0][0] +1, self.points[0][1] ))
            
            else : 
                self.points.append((self.points[0][0] -1 , self.points[0][1]))
                self.points.append((self.points[0][0] +1, self.points[0][1] + 2))

        self.sortValues()
        for i in self.points:
            surface.stateSet(self.index,i)

#
# ---- Long ----
# 
# schéma : 
#
#   0 0 0  
#     

class Long(Piece):
    def __init__(self, pos, index, surface: Grille) -> None:
        super().__init__(pos, index, surface)

        if self.points[0][0] > 5:
            self.points.append((self.points[0][0] -1 , self.points[0][1] + 2))
            self.points.append((self.points[0][0] -2 , self.points[0][1] + 4))

        elif self.points[0][0] > 4:
            self.points.append((self.points[0][0] -1 , self.points[0][1] + 2))
            self.points.append((self.points[0][0] -2 , self.points[0][1] + 2))

        
        else:
            self.points.append((self.points[0][0] -1 , self.points[0][1]))
            self.points.append((self.points[0][0] -2 , self.points[0][1]))

        self.sortValues()
        for i in self.points:
            surface.stateSet(self.index,i)

#
# ---- Crochet ----
# 
# schéma : 
#
#   0      0
#    0 ou 0
#    0    0
#    

class Crochet(Piece):
    def __init__(self, pos, index, surface: Grille,reverse = False) -> None:
        super().__init__(pos, index, surface)
        if reverse:
            if self.points[0][0] < 4:
                self.points.append((pos[0]+1,pos[1]+1))
            else: self.points.append((pos[0]+1,pos[1]-1))


        else:
            self.points.append((self.points[0][0], self.points[0][1] + 1))



        if self.points[1][0] >= 4:
            self.points.append((self.points[1][0] +1 , self.points[1][1]))

        else:
            self.points.append((self.points[1][0] +1 , self.points[1][1] + 2))

        self.sortValues()
        for i in self.points:
            surface.stateSet(self.index,i)


#
# ---- Fleche ----
# 
# schéma : 
#
#   0      
#  0 0 
#        
#   

class Fleche(Piece):
    def __init__(self, pos, index, surface: Grille) -> None:
        super().__init__(pos, index, surface)
        self.points.append((self.points[0][0], self.points[0][1] + 1))
        if self.points[0][0] >= 4 :
            self.points.append((self.points[0][0]+1, self.points[0][1] - 1))

        else : self.points.append((self.points[0][0] +1 , self.points[0][1] + 1))

        self.sortValues()
        for i in self.points:
            surface.stateSet(self.index,i)

