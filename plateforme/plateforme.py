import pygame

UP = (0,-1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Plateforme(pygame.sprite.Sprite):
    def __init__(self, x, y, height, width, image_path, lumiere):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.height = height
        self.width = width
        self.lumiere = lumiere
        self.direction = None
        self.direction2 = None
        self.max_distance = None
        
    def apparition(self, opacite, surface):
        if self.lumiere == True and opacite <= 120 :
            surface.blit(self.image, self.rect)
            self.draw(surface)

    def deplacement(self, vitesse, direction_x=None, direction_y=None, max_distance=None):
        
        self.direction = direction_x
        self.direction2 = direction_y
        self.max_distance = max_distance

        #mouvement
        if self.direction == RIGHT:
            self.rect.x += vitesse
            self.distance_moved += vitesse 
        elif self.direction == LEFT:
            self.rect.x -= vitesse
            self.distance_moved += vitesse
        if self.direction2 == UP:
            self.rect.y -= vitesse
            self.distance_moved += vitesse
        elif self.direction2 == DOWN:
            self.rect.y += vitesse
            self.distance_moved += vitesse


        #demi-tour
        if self.distance_moved >= self.max_distance:
            
            if self.direction == RIGHT:
                self.direction = LEFT
            elif self.direction == LEFT:
                self.direction = RIGHT
                
            if self.direction2 == UP:
                self.direction2 = DOWN
            elif self.direction2 == DOWN:
                self.direction2 = UP
                
            self.distance_moved = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
        