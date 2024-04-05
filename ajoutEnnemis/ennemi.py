import pygame
import random
import math
import time

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



class Projectiles:
    def __init__(self, x, y, width, height, direction):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.direction = direction
        self.speed = 5  # Ajouter une vitesse pour les projectiles
        self.rect = pygame.Rect(x, y, width, height)  # Ajouter un rectangle pour les projectiles

    def moveFront(self):
        if self.direction == 'right':
            self.x += self.speed
        elif self.direction == 'left':
            self.x -= self.speed
        self.rect.x = self.x  # Mettre à jour le rectangle

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

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

def tirer(perso, ennemi):
    ecart = math.hypot(ennemi.rect.x - perso.position[0], ennemi.rect.y - perso.position[1])

    if ecart <= 100:
        if ennemi.side == "left":
            nouveau_projectile = Projectiles(ennemi.rect.x, ennemi.rect.y, 20, 10, ennemi.side)
        else :
             nouveau_projectile = Projectiles(ennemi.rect.x + ennemi.width, ennemi.rect.y, 20, 10, ennemi.side)
        return nouveau_projectile

    return None


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake")

def main():
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Snake")

    clock = pygame.time.Clock()
    ennemiTir = Ennemi(160, 160, 40, 40, "SpritemonstreExemple.png")
    ennemiCourt = Ennemi(160, 280, 40, 40, "SpritemonstreExemple.png")
    
    projectile_timer = time.time()
    projectiles = []

    while True:

        screen.fill((255,255,255))
        ennemiCourt.draw(screen)
        ennemiTir.draw(screen)
        
        ennemiCourt.deplacer()
        ennemiCourt.collision("plateforme") #l'objet plateforme sur lequel il se trouve 
        
        if time.time() - projectile_timer >= 2:
            tir = tirer("perso", ennemiTir) #mettre notre personnage en tant qu'attribut
            if tir:
                projectiles.append(tir)
                projectile_timer = time.time()

        for tir in projectiles:
            tir.moveFront()
            tir.draw(screen)

            if tir.x < 0 or tir.x > screen_width or tir.y < 0 or tir.y > screen_height:
                projectiles.remove(tir)

        ennemiTir.update("perso") 
        pygame.display.update()
        clock.tick(10)

if __name__ == "__main__":
    
    main()