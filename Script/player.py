import pygame


class Entity(pygame.sprite.Sprite):

    def __init__(self, x, y, game):
        super().__init__()
        self.game = game

        self.position = [x, y]
        self.velocity = 5

        self.old_position = self.position.copy()

    def check_collisions(self, sprite, group):
        for other_sprite in group:
            if sprite != other_sprite and pygame.sprite.collide_rect(sprite, other_sprite):
                return True
        return False

    def move_right(self):
        self.position[0] += self.velocity
        if self.check_collisions(self, self.game.all_grounds):
            self.position[0] -= self.velocity

    def move_left(self):
        self.position[0] -= self.velocity
        if self.check_collisions(self, self.game.all_grounds):
            self.position[0] += self.velocity

    def update(self):
        self.rect.topleft = self.position


class Player(Entity):

    def __init__(self, x, y, image_path, width, height, game):
        super().__init__(x, y, game)

        # Information about player
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

    def draw(self, surface):
        # Load image
        surface.blit(self.image, self.rect)


class Enemy(Entity):

    def __init__(self, x, y, image_path, width, height, game):
        super().__init__(x, y, game)

        # Information about player
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

    def draw(self, surface):
        # Load image
        surface.blit(self.image, self.rect)

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.original_image = pygame.image.load("Asset/bossTest.png").convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (600,500))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 0
        self.time_since_mouvement = 0.0 
        self.time_since_attack = 0.0 
        self.air_resistance = 1
        self.velocity = 5      
        self.inMouvement = False 
        self.attack = False 
    
    def move(self,top):
        if top :
            self.velocity -=20
        else:
            self.velocity += 20
        
        self.time_since_mouvement = 0.0 

    def update(self,deltatime):
        #Block deplacement
        if self.velocity !=  0:
            self.rect.y += self.velocity

            if self.velocity > 0:
                self.velocity -= self.air_resistance
            else :
                self.velocity += self.air_resistance

        elif self.inMouvement and self.velocity == 0: # Vecteur de deplacement a zero
            self.inMouvement = False
            self.time_since_mouvement = 0.0 

        else:
            self.time_since_mouvement += deltatime
            self.time_since_attack += deltatime

        if self.time_since_mouvement >= 5.0: # Le temps entre chaque deplacement
            self.inMouvement = True
            if self.rect.y < 0:
                self.move(True)   # La logique de mouvement est a revoir pour pas qu'il quite l'ecran
            else:
                self.move(False)
        #Block deplacement
        # Oui c'est factorisable si tes pas content fais le 

        if not self.inMouvement and self.attack:
            self.time_since_attack == 0.0 
            print("attaque")
            self.attack = False

        elif self.time_since_attack >= 2.5:
            self.attack = True
            self.time_since_attack = 0.0
        else:
            self.time_since_attack += deltatime
