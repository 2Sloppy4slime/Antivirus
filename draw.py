import pygame
import entities
import random
margin = 200 # ne respecte pas programmation fonctionelle mais est bien plus pratique que de réécrire a chaque fois

def drawGrid(surface):
    currenty = margin
    currentx = margin
    offsetx = 0
    offsety = 0
    fond = pygame.image.load("point_vide.png")
    for x in range(4):

        for y in range(4):
            #base
            surface.blit(fond,(currentx + offsetx -30 ,currenty + offsety -30))

            if y<3 and x<3:
                surface.blit(fond,(currentx + offsetx +20 ,currenty + offsety +20))
            offsety += 100
        offsety = 0
        offsetx += 100
        pygame.draw.circle(surface,"black",(150,150),30) #base
        pygame.draw.circle(surface,"white",(150,150),28)

def checkGrid(surface, grille: entities.Grille, selectedindex = 1):
    #ces valeurs la sont les positions possibles des point d'une ligne dans l'ordre (de haut gauche à bas droite)
    posrow1 = [(500,200)]
    posrow7 = [(200,500)]

    posrow2 = [(400,200),(450,250),(500,300)]
    posrow6 = [(200,400),(250,450),(300,500)]

    posrow3 = [(300,200),(350,250),(400,300),(450,350),(500,400)]
    posrow5 = [(200,300),(250,350),(300,400),(350,450),(400,500)]

    posrow4 = [(200,200),(250,250),(300,300),(350,350),(400,400),(450,450),(500,500)]
    
    screen2 = pygame.Surface((80,80),pygame.SRCALPHA )
    screen2.set_alpha(50)
    
    
    for i in range(1,8):
        match i:

            #---------------------------------------------------------------------------------------------------------
            # On regarde d'abord ceux qui n'ont qu'un element dans leur ligne:
            #---------------------------------------------------------------------------------------------------------
            case 1:

                if grille.stateOf((1,0)) == 0 : 
                    pass
                else :
                    surface.blit(getpusscolor(grille.stateOf((1,0))),(posrow1[0][0] -30,posrow1[0][1] -30) )
                    if selectedindex +2 == grille.stateOf((1,0)):
                        pygame.draw.circle(screen2,drawcolorget(grille.stateOf((1,0))),(40,40),35)
                        surface.blit(screen2, (posrow1[0][0]-40,posrow1[0][1]-40))
            
            case 7:
                
                if grille.stateOf((7,0)) == 0 : 
                    
                    pass
                else :
                    
                    surface.blit(getpusscolor(grille.stateOf((7,0))),(posrow7[0][0] -30,posrow7[0][1] -30) )
                    if selectedindex +2 == grille.stateOf((7,0)):
                        pygame.draw.circle(screen2,drawcolorget(grille.stateOf((7,0))),(40,40),35)
                        surface.blit(screen2, (posrow7[0][0]-40,posrow7[0][1]-40))
                    
            




            #---------------------------------------------------------------------------------------------------------
            # Puis ceux qui en ont 3:
            #---------------------------------------------------------------------------------------------------------
            case 2:
                for i in range(len(grille.rows["2"])):
                  
                    if grille.stateOf((2,i)) == 0 : 
                        pass
                    else :
                        surface.blit(getpusscolor(grille.stateOf((2,i))),(posrow2[i][0] -30,posrow2[i][1] -30) )  
                        if selectedindex +2 == grille.stateOf((2,i)):
                            pygame.draw.circle(screen2,drawcolorget(grille.stateOf((2,i))),(40,40),35)
                            surface.blit(screen2, (posrow2[i][0]-40,posrow2[i][1]-40))
            
            case 6:
                for i in range(len(grille.rows["6"])):
                    if grille.stateOf((6,i)) == 0 : 
                        pass
                    else :
                        surface.blit(getpusscolor(grille.stateOf((6,i))),(posrow6[i][0] -30,posrow6[i][1] -30) )
                        if selectedindex +2 == grille.stateOf((6,i)):
                            pygame.draw.circle(screen2,drawcolorget(grille.stateOf((6,i))),(40,40),35)
                            surface.blit(screen2, (posrow6[i][0]-40,posrow6[i][1]-40))





            #---------------------------------------------------------------------------------------------------------
            # Puis ceux qui en ont 5:
            #---------------------------------------------------------------------------------------------------------
            case 3:
                for i in range(len(grille.rows["3"])):
                    if grille.stateOf((3,i)) == 0 : 
                        pass
                    else :
                        surface.blit(getpusscolor(grille.stateOf((3,i))),(posrow3[i][0] -30,posrow3[i][1] -30) )
                        if selectedindex +2 == grille.stateOf((3,i)):
                            pygame.draw.circle(screen2,drawcolorget(grille.stateOf((3,i))),(40,40),35)
                            surface.blit(screen2, (posrow3[i][0]-40,posrow3[i][1]-40))

            case 5:
                for i in range(len(grille.rows["5"])):
                    if grille.stateOf((5,i)) == 0 : 
                        pass
                    else :
                        surface.blit(getpusscolor(grille.stateOf((5,i))),(posrow5[i][0] -30,posrow5[i][1] -30) )
                        
                        if selectedindex +2 == grille.stateOf((5,i)):
                            pygame.draw.circle(screen2,drawcolorget(grille.stateOf((5,i))),(40,40),35)
                            surface.blit(screen2, (posrow5[i][0]-40,posrow5[i][1]-40))





            #---------------------------------------------------------------------------------------------------------
            # Puis celui qui en a 7:
            #---------------------------------------------------------------------------------------------------------
            case 4:
                for i in range(len(grille.rows["4"])):
                  
                    if grille.stateOf((4,i)) == 0 : 
                        pass
                    else :
                         
                        surface.blit(getpusscolor(grille.stateOf((4,i))),(posrow4[i][0] -30,posrow4[i][1] -30) )
                        if selectedindex +2 == grille.stateOf((4,i)):
                            pygame.draw.circle(screen2,drawcolorget(grille.stateOf((4,i))),(40,40),35)
                            surface.blit(screen2, (posrow4[i][0]-40,posrow4[i][1]-40))
                            
                            



def drawcolorget(num):
    match num: # on assume que le nombre maximal de pièces est 9
        case 0:
            return "white"
        case 1:
            return (30,15,35)
        case 2:
            return "red"
        case 3:
            return "yellow"
        case 4:
            return  "green"
        case 5:
            return "yellow"
        case 6:
            return "orange"
        case 7:
            return (255,130,255)
        case 8:
            return "cyan"
        case 9:
            return "green"
        case _:
            return "purple"

def getpusscolor(num):
    match num: # on assume que le nombre maximal de pièces est 9

        case 1:
            return pygame.image.load("py_gray.png")
        case 2:
            return pygame.image.load("py_red.png")
        case 3:
            return pygame.image.load("py_yellow.png")
        case 4:
            return  pygame.image.load("py_green.png")
        case _:
            return pygame.image.load("py_green.png")
                        
    