

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
    #pour représenter la position d'un point dans la grille, on utilise un tuple (row, index) donc (1,0) serait le coin en haut à droite
    #to represent the position of a point in the grid, we use a tuple (row,index) so (1,0) would be the top right corner
    #-----------------------------------------------------

    
    def __init__(self) -> None:
        self.rows = {}
        self.rows["1"] =       [0] #Here's how we see the grid
        self.rows["2"] =     [0,0,0] #every number represents the state of a position in the grid e.g : 0 = empty
        self.rows["3"] =   [0,0,0,0,0]#a good way would be to use a single list but this feels a little less confusing
        self.rows["4"] = [0,0,0,0,0,0,0] #voici comment on voit la grille
        self.rows["5"] =   [0,0,0,0,0] #chaque nombre représente l'état actuel de la case : 0 = vide
        self.rows["6"] =     [0,0,0] #un meilleur moyen serait de ne faire qu'une seule liste mais cela serait un peu plus confus, ici, tout est clair niveau mouvement
        self.rows["7"] =       [0]
        self.exit =[0] #this value is useful outside of the grid


    def stateOf(self,pos = (1,0)) -> int: #Returns the State of the position on the grid based on the given coordinates.
        '''-> Int  | Returns the State of the position on the grid based on the given coordinates. \n it is to note that a value of 0 is an empty space and 1 is an immovable object'''
        
        if pos[1] < len(self.rows[str(pos[0])]) and pos[1] > -1 :
            return self.rows[str(pos[0])][pos[1]]
        
        else : raise IndexError("Tried to get a value from out of bounds") #throws an Error if the function goes out of bounds

    def stateSet(self,index,pos = (1,0)) -> None : #Sets the State of a position on the grid based on the given coordinates
        '''-> None  | Sets the State of a position on the grid based on the given coordinates'''

        if pos[1] < len(self.rows[str(pos[0])]) and pos[1] > -1 :
            self.rows[str(pos[0])][pos[1]] = index
        
    def reset(self) -> None :
        ''' -> None  | Resets The Grid'''

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
#Here we define our base pieces :
#---------------------------------------------------------------------------------------------------------------------------------------------------------------      
        

#Base Object for everything that can move
class Piece(): #Objet de base pour tout GameObject qui bouge

    def sortValues(self):
        self.points = sorted(self.points)


    def __init__(self,pos,index,surface: Grille,rotation = "ul") -> None:
        self.rotation = rotation
        self.index = index
        self.points = [pos]
        self.sortValues() #inutile ici mais sert de modèle pour faire les autres
        for i in self.points:
            surface.stateSet(self.index,i)
        
    

    def mvtHorizontal(self,amount,surface : Grille, entitylist): #horizontal par rapport au losange au dessus donc dans ce sens là : "\" pour la grille graphique
        snd_moved = pygame.mixer.Sound("SND\canmove.mp3")
        snd_stopped = pygame.mixer.Sound("SND\cantmove.mp3")
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





#le virus, pièce principale du jeu
#virus, main piece of the game
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
#here we define our building pieces : 
#---------------------------------------------------------------------------------------------------------------------------------------------------------------

#tired of translating this just read the schematics and the names

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
    def __init__(self, pos, index, surface: Grille,rotation = "up") -> None:
        super().__init__(pos, index, surface,rotation)
        if self.rotation == "up" or self.rotation == "left":
            self.points.append((pos[0],pos[1]+1))
        else:
            if self.points[0][0] < 4:
                self.points.append((pos[0]+1,pos[1]+1))
            else: self.points.append((pos[0]+1,pos[1]-1))
        

        self.sortValues()
        for i in self.points:
            surface.stateSet(self.index,i)


#
# ---- droite/straight ----
# 
# schéma : 
#
#   0   ou  0  0
#   0


class Droite(Piece):
    def __init__(self, pos, index, surface: Grille,rotation = "up") -> None:
        super().__init__(pos, index, surface,rotation)
        if self.rotation == "up" or self.rotation == "down":
            
            if self.points[0][0] >= 4:
                self.points.append((self.points[0][0] +1 , self.points[0][1]))

            else:
                self.points.append((self.points[0][0] +1 , self.points[0][1] + 2))
        else:
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

