
import pygame
import entities
import draw
import levelmanager

pygame.init()
binds = open("keybinds.opt","r")
lines  = binds.readlines()
binds.close()

lines.pop(8)
lines.pop(6)
lines.pop(4)
lines.pop(2)
lines.pop(0)
nulines = []
for i in lines:
    if len(i) > 1:
        nulines.append(i[0])
    else : nulines.append(i)


UpLeft = pygame.key.key_code(nulines[0])
UpRight = pygame.key.key_code(nulines[1])
DownRight = pygame.key.key_code(nulines[2])
DownLeft = pygame.key.key_code(nulines[3])
Selector = pygame.key.key_code(nulines[4])


def main() -> None:
    
    pygame.init()
    screensize = (720,720)
    screen = pygame.display.set_mode(screensize)
    clock = pygame.time.Clock()
    pygame.display.set_caption("[A N T I V I R U S]","[AV]")
    icon = pygame.image.load("GFX\icon.png").convert_alpha()
    pygame.display.set_icon(icon)

    menubg = pygame.image.load("GFX\menubg.png")
    diffbg = pygame.image.load("GFX\menubg2.png")
    bg = pygame.image.load("GFX\gamebg.png")
    vignette = pygame.image.load("GFX\ignette.png").convert_alpha()
    win = pygame.image.load("GFX\win.png").convert_alpha()


    running = True
    gameState = 0
    
    
    grille = entities.Grille()
    difficultymultiplier = 0 
    entitylist = []
    selectIndex = 0
    choosingdiff = False
    menurendered = False
    currentlevel = 1
    levelloaded = False
    tutorial_level = True

    
    
    pygame.mixer.init()

    

    while running:
        
        if gameState == 1:
            if levelloaded == False:
                currentlevel = currentlevel + 50 * difficultymultiplier
                entitylist = levelmanager.load(currentlevel,grille)
                levelloaded = True
            
            # processing des events
            for event in pygame.event.get():
                
                if event.type == pygame.KEYDOWN:
                    if event.key == Selector: #changer l'index de mouvement
                        if selectIndex + 1< len(entitylist) :
                            selectIndex += 1
                        else :selectIndex = 0
                        
                        #mouvement horizontal
                    if event.key == UpLeft:
                        
                        entitylist[selectIndex].mvtHorizontal(-1,grille,entitylist)
                        if grille.exit[0] == 1: #gagné
                            screen.blit(win, (0, 0))
                            gameState = 2
                            


                    if event.key == DownLeft:
                        entitylist[selectIndex].mvtHorizontal(1,grille,entitylist)



                        #mouvement vertical
                    if event.key == DownRight:
                        entitylist[selectIndex].mvtVertical(1,grille,entitylist)
                    
                    if event.key == UpRight:
                        entitylist[selectIndex].mvtVertical(-1,grille,entitylist)

                    
                    if event.key == pygame.K_ESCAPE:
                        grille.reset()
                        gameState = 0
                        choosingdiff = False
                        menurendered = False
                        currentlevel = 1
                        levelloaded = False
                        tutorial_level = True
                        difficultymultiplier = 0

                if event.type == pygame.QUIT:
                    running = False

            # estompe le reste
            
            screen.blit(bg, (0, 0))

            # RENDER
            draw.drawGrid(screen)
            draw.checkGrid(screen,grille,selectIndex)
            screen.blit(vignette, (0, 0))
            if grille.exit[0] == 1:
                print("win")
                screen.blit(win,(0,0))

            # flip pour display
            pygame.display.flip()
            
        elif gameState == 0:
            
            if menurendered == False:
                screen.blit(menubg, (0,0))
                pygame.display.flip()
                
                menurendered = True

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if choosingdiff == True:
                        if event.key == pygame.K_e:
                            gameState = 1
                        if event.key == pygame.K_t:
                            difficultymultiplier = 1
                            gameState = 1
                        if event.key == pygame.K_c:
                            difficultymultiplier = 2
                            gameState = 1
                        if event.key == pygame.K_b:
                            difficultymultiplier = 3
                            gameState = 1
                    if event.key == pygame.K_SPACE:
                        screen.blit(diffbg, (0,0))
                        choosingdiff = True
                        pygame.display.flip()
                        
                if event.type == pygame.QUIT:
                        running = False
        
        elif gameState == 2:
            for event in pygame.event.get():    
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        currentlevel += 1
                        
                        entitylist = levelmanager.load(currentlevel,grille)
                        gameState = 1
                
        clock.tick(60)  # limite FPS à 60
    

    pygame.quit()

main()
