import pygame
import math
import time

screen_width = 800
screen_height = 600

UP = (0,-1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Ennemi(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)  # charge l'image de l'ennemi
        self.image = pygame.transform.scale(self.image, (width, height))  # redimensionne l'image si nécessaire
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.angle = 0
        self.side = None
        self.speed = 2
        self.direction = RIGHT

    def update(self, perso):
        dx = perso.position[0] - self.rect.x
        if dx < 0:
            side = 'left'
        elif dx > 0:
            side = 'right'
        else:
            side = None

        if side != self.side:
            self.side = side
            if self.side == 'left':
                self.angle += math.pi  # Ajouter pi pour tourner vers la gauche
            elif self.side == 'right':
                self.angle -= math.pi
                
    def deplacer(self):
        if self.direction == RIGHT:
            self.rect.x += self.speed
        elif self.direction == LEFT:
            self.rect.x -= self.speed
        
    def collision(self, plateforme):
        if self.rect.right >= screen_width or self.rect.left <= 0 or self.rect.right >= plateforme.rect.right or self.rect.left <= plateforme.rect.left: ##a modifier selon les éléments de collisions
            if self.direction == RIGHT:
                self.direction = LEFT
            elif self.direction == LEFT:
                self.direction = RIGHT

    def draw(self, surface):
        if self.side == 'left' or self.direction == LEFT:
            flipped_image = pygame.transform.flip(self.image, True, False)
            surface.blit(flipped_image, self.rect)
        else:
            surface.blit(self.image, self.rect)
            
        