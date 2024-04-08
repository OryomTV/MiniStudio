import pygame

pygame.init()

screen_width = 800
screen_height = 600

grid_size = 20
grid_width = screen_width/grid_size
grid_height = screen_height/grid_size

UP = (0,-1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

from monstre import Ennemi
from plateforme import Plateforme


def main():
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Snake")
    
    clock = pygame.time.Clock()
    ennemiCourt = Ennemi(160, 245, 40, 40, "SpritemonstreExemple.png")
    
    plateformeDiagonale = Plateforme(300, 100, 15, 40, "plateforme.png", False)
    plateformeDiagonale.distance_moved = 0 
    plateformeDiagonale.direction = RIGHT #direction au lancement
    plateformeDiagonale.direction2 = DOWN

    plateformeMonstre = Plateforme(160, 285, 15, 70, "plateforme.png",False)

    while True:

        screen.fill((255,255,255))
        plateformeDiagonale.draw(screen)
        plateformeMonstre.draw(screen)
        
        plateformeDiagonale.deplacement(2, plateformeDiagonale.direction, plateformeDiagonale.direction2, 60)

        ennemiCourt.draw(screen)
        
        ennemiCourt.deplacer()
        ennemiCourt.collision(plateformeMonstre) #l'objet plateforme sur lequel il se trouve 
        
        pygame.display.update()
        clock.tick(10)

if __name__ == "__main__":
    
    main()