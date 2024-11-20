import entities


def load(id: int, grille : entities.Grille):
    entitylist = []
    grille.reset()
    match id:
        
        case 1 :
            #murs
            grille.stateSet(1,(4,4))
            #virus
            entitylist.append(entities.Virus((4,2),grille))
            #autres pièces
            entitylist.append(entities.Coin((4,1),3,grille,True))
            
            #return
            return entitylist
        
        case 2:
            #murs
            grille.stateSet(1,(3,1))
            grille.stateSet(1,(4,3))
            #virus
            entitylist.append(entities.Virus((2,1),grille))
            #autres pièces
            entitylist.append(entities.Diagonale((4,1),3,grille,True))
            
            #return
            return entitylist
        

        case 51:
            #murs
            
            grille.stateSet(1,(4,3))
            #virus
            entitylist.append(entities.Virus((3,2),grille))
            #autres pièces
            entitylist.append(entities.Verticale((4,4),3,grille))
            entitylist.append(entities.Fleche((2,0),4,grille))
            
            #return
            return entitylist
        case _ : 
            #murs
            grille.stateSet(1,(2,1))
            #virus
            entitylist.append(entities.Virus((4,5),grille))
            #autres pièces
            entitylist.append(entities.Crochet((3,3),3,grille,True))
            entitylist.append(entities.Fleche((5,1),4,grille))
            #return
            return entitylist
            