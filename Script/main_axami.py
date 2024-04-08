import pygame
import math 
pygame.init()

screen_width = 800
screen_height = 600

grid_size = 20
grid_width = screen_width/grid_size
grid_height = screen_height/grid_size

# Création de la surface pour le menu pause 
pause_rectangle = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
pause_rectangle.fill((0,0,255))

opacite = 128  
pause_rectangle.set_alpha(opacite)

UP = (0,-1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Menu:
        def __init__(self):
            self.principal = True
            self.pause = False
            self.parametre = False
        
        def menuActive(self):
            if self.principal or self.pause or self.parametre:
                return True
            else:
                return False
        
        def menuPrincipal(self):
            #Importer le background 
            fondEcranMenu = pygame.image.load("moutagneBackgound.png")
            fondEcranMenu = pygame.transform.scale(fondEcranMenu,(screen_width,screen_height))

            #Importer l'image play du boutton
            play_button = pygame.image.load("jouer.png")
            play_button = pygame.transform.scale(play_button,(360,180))
            play_button_rect = play_button.get_rect()
            play_button_rect.x =  math.ceil(screen_width / 4)
            play_button_rect.y =  math.ceil(screen_width / 3)

            #Importer l'image du boutton quit
            quit_button = pygame.image.load("bouttonQuitMenu.png")
            quit_button = pygame.transform.scale(quit_button,(200,200))
            quit_button_rect = quit_button.get_rect()
            quit_button_rect.x =  math.ceil(screen_width / 4)
            quit_button_rect.y =  math.ceil(screen_width / 2)

            screen.blit(fondEcranMenu,(0,0))
            screen.blit(play_button,play_button_rect)
            screen.blit(quit_button,quit_button_rect)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if play_button_rect.collidepoint(event.pos):
                        self.principal = False
                    elif quit_button_rect.collidepoint(event.pos):
                        pygame.quit()

                elif event.type == pygame.QUIT:
                    pygame.quit()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake")

def main():
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Snake")


    clock = pygame.time.Clock()

    #snake = Snake()
    menu = Menu()

    while True:

        if not menu.menuActive():
            #Le code principal ici 
            screen.fill((255,255,255))
            menu.pause = snake.handle_keys()  #snake.handle_keys() retourne True si Z a etait presser sinon return rien
            snake.move()
            snake.draw(screen)

        elif menu.pause:            
            #Menu pause
            screen.fill((255,255,255))
            snake.draw(screen)  # besoin de snake pour la pause (pour l'afficher deriere le fond bleu) donc pas encore facto
            screen.blit(pause_rectangle, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu.pause = False
        else:
            #Ecran principal
            menu.menuPrincipal()
            
        pygame.display.update()

        clock.tick(10)

if __name__ == "__main__":
    main()