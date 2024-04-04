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


def distance(x, y):
    return ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** 0.5

def Filtre(surface, transparence, rayon, objet):
    filtre_noire = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    filtre_noire.fill((0, 0, 0, 60)) ##le filtre autour de l'objet
    
    surface.blit(filtre_noire, (0, 0))
    
    if objet is not None: ##si appliqué autour d'un objet
        filtre_objet = pygame.Surface(surface.get_size(), pygame.SRCALPHA) 
        filtre_objet.fill((0, 0, 0, transparence//2)) ##va appliqué ce filtre tout autour de l'objet
        pygame.draw.circle(filtre_objet, (0, 0, 0, 0), objet, rayon) #la taille du cercle de limiere autour de l'objet
        surface.blit(filtre_objet, (0, 0)) ##affiche le filtre
    else:
        filtre_noire = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        filtre_noire.fill((0, 0, 0, transparence))
        surface.blit(filtre_noire, (0, 0))


class Snake:
    def __init__(self):
        self.length = 1
        self.position = [screen_width // 2, screen_height // 2]
        self.direction = RIGHT
        self.rect = pygame.Rect(self.position, (grid_size,grid_size))

    def turn(self, point):
        self.direction = point

    def move(self):
        current = self.position
        x, y = self.direction
        new = (current[0] + x * grid_size), (current[1] + y * grid_size)
        self.position = new
        self.rect = pygame.Rect(self.position, (grid_size,grid_size))

    def draw(self, surface):
        pygame.draw.rect(surface, (0,255,0), self.rect)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                if event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                if event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)
                if event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                    

class Fruit:
    def __init__(self):
        self.position = (20,20)
        self.rect = pygame.Rect(self.position, (grid_size,grid_size))

    def random_position(self):
        self.position = ((random.randint(0, grid_width - 1) * grid_size),(random.randint(0, grid_height - 1) * grid_size))
        self.rect = pygame.Rect(self.position, (grid_size,grid_size))
   
    def draw(self, surface):
        pygame.draw.rect(surface, (0,0,255), self.rect)


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

    def update(self, snake):
        dx = snake.position[0] - self.rect.x
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

        
    def collision(self):
        if self.rect.right >= screen_width or self.rect.left <= 0: ##a modifier selon les éléments de collisions
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

def tirer(snake, ennemi):
    ecart = math.hypot(ennemi.rect.x - snake.position[0], ennemi.rect.y - snake.position[1])

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
    opacity = 225
    snake = Snake()
    fruit = Fruit()
    ennemiTir = Ennemi(160, 160, 40, 40, "SpritemonstreExemple.png")
    ennemiCourt = Ennemi(160, 280, 40, 40, "SpritemonstreExemple.png")
    
    projectile_timer = time.time()
    projectiles = []

    while True:

        screen.fill((255,255,255))
        snake.handle_keys()
        snake.move()
        snake.draw(screen)
        fruit.draw(screen)
        ennemiCourt.draw(screen)
        ennemiTir.draw(screen)
        Filtre(screen, opacity, 50, snake.rect.center)
        
        ennemiCourt.deplacer()
        ennemiCourt.collision()
        
        if time.time() - projectile_timer >= 2:
            tir = tirer(snake, ennemiTir)
            if tir:
                projectiles.append(tir)
                projectile_timer = time.time()

        for tir in projectiles:
            tir.moveFront()
            tir.draw(screen)

            if tir.x < 0 or tir.x > screen_width or tir.y < 0 or tir.y > screen_height:
                projectiles.remove(tir)

        if snake.rect.colliderect(fruit.rect):
            opacity -= 40
            fruit.random_position()

        ennemiTir.update(snake)
        pygame.display.update()
        clock.tick(10)

if __name__ == "__main__":
    
    main()