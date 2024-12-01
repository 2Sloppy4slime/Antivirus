import entities


def load(id: int, grille : entities.Grille):
    entitylist = []
    grille.reset()
    
    match id:
        
        case 1 :
            #murs
            a=1
            grille.stateSet(1,(4,4))
            #virus
            entitylist.append(entities.Virus((4,2),grille))
            #autres pièces
            entitylist.append(entities.Coin((4,1),3,grille,True))
            
            #return
            return entitylist
        
        case 2:
            #murs
            a=2
            grille.stateSet(1,(3,1))
            grille.stateSet(1,(4,3))
            #virus
            entitylist.append(entities.Virus((2,1),grille))
            #autres pièces
            entitylist.append(entities.Diagonale((4,1),3,grille,"down"))
            
            #return
            return entitylist
        

        case 51:
            #murs
            a=51
            grille.stateSet(1,(4,3))
            #virus
            entitylist.append(entities.Virus((3,2),grille))
            #autres pièces
            entitylist.append(entities.Droite((4,4),3,grille))
            entitylist.append(entities.Fleche((2,0),4,grille))
            
            #return
            return entitylist
        case 52 : 
            #murs
            a=52
            grille.stateSet(1,(2,1))
            #virus
            entitylist.append(entities.Virus((4,5),grille))
            #autres pièces
            entitylist.append(entities.Crochet((3,3),3,grille,True))
            entitylist.append(entities.Fleche((5,1),4,grille))
            #return
            return entitylist

        case _ :
            print("invalid level ID found. Standby mode")


def getLevelList()  :
    a = open("level_list.lvl","r")
    b = a.readlines()
    a.close()

    levellist = [] # a list containing level strings and their respective ID in a tuple : (id,levelscript)
    for i in b:
        if "import" in i or "OS" in i or "exec" in i or "open" in i or "draw" in i or "main" in i or "levelmanager" in i or "pygame" in i: #trying my best to avoid malicious code in here
            raise PermissionError("tried to import potentially malicious code")
        if "entitylist" in i and "grille" in i :
            c = i.split(";")[0]
            levellist.append((int(c[2:]),i))
        else:
            raise SyntaxError("level does not contain key elements of level making")

    
    return levellist
            