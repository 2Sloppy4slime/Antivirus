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
            entitylist.append(entities.Coin((4,1),3,grille,"right"))
            
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



def interpretLevelCode(string : str, grille : entities.Grille): # this interprets code safely to give a levelloader script (  so in the file rock@4,0 will turn into "grille.stateSet(1,(4,0));"   )

    codelist = string.split(";")
    #levelstring = "entitylist=[];"
    levelstring = ""
    currententityindex = 3
    for i in codelist: # code is written as [type],[rotation]@position1,position2
        match i :
            case i if "rock" in i :
                levelstring += f"grille.stateSet(1,({i[-3]},{i[-1]}));" #index is hardcoded since we can't have coordinates bigger than 7
            

            case i if "virus" in i :
                levelstring += f"entitylist.append(entities.Virus(({i[-3]},{i[-1]}),grille));"
            

            case i if "straight" in i:
                levelstring += f"entitylist.append(entities.Droite(({i[-3]},{i[-1]}),{currententityindex},grille,\"{i[9:-4]}\"));"
                currententityindex += 1


            case i if "corner" in i:
                levelstring += f"entitylist.append(entities.Coin(({i[-3]},{i[-1]}),{currententityindex},grille,\"{i[7:-4]}\"));"
                currententityindex += 1


            case i if "long" in i:
                levelstring += f"entitylist.append(entities.Long(({i[-3]},{i[-1]}),{currententityindex},grille,\"{i[5:-4]}\"));"
                currententityindex += 1


            case i if "diagonal" in i:
                levelstring += f"entitylist.append(entities.Diagonale(({i[-3]},{i[-1]}),{currententityindex},grille,\"{i[9:-4]}\"));"
                currententityindex += 1

            case i if "arrow" in i:
                levelstring += f"entitylist.append(entities.Fleche(({i[-3]},{i[-1]}),{currententityindex},grille,\"{i[6:-4]}\"));"
                currententityindex += 1

            case i if "hook" in i:
                levelstring += f"entitylist.append(entities.Crochet(({i[-3]},{i[-1]}),{currententityindex},grille,\"{i[5:-4]}\"));"
                currententityindex += 1
    
    return levelstring



def getLevelList(grille : entities.Grille)  :
    a = open("level_list.lvl","r")
    b = a.readlines()
    a.close()

    levellist = [] # a list containing level strings and their respective ID in a tuple : (id,levelscript)
    for i in b:
        c = i.split(";")[0]
        levellist.append((int(c[2:]),interpretLevelCode(i,grille)))


    
    return levellist


def loadLevelFromID(id,grille: entities.Grille):
    grille.reset()
    levellist = getLevelList(grille)
    entitylist = []
    for i in levellist : 
        if i[0] == id :
            exec(i[1],{'grille':grille, 'entities': entities , 'entitylist': entitylist})
    return entitylist

            