import entities

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

            