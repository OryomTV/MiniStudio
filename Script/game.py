# game.py
import pygame
from square import Square
from ground import Ground

class Game:
    def __init__(self):
        pygame.display.set_caption("Shining")
        self.screen = pygame.display.set_mode((1920, 1080))
        self.background = pygame.image.load("Kingdom Hearts 3_2.jpg")

        self.rect = self.background.get_rect()
        self.rect.x = 600
        self.rect.y = 700
        self.velocity = 1

        self.square1 = Square(self.rect.x, self.rect.y, 30, 30, (0, 0, 255), self)
        self.square2 = Square(self.rect.x + 250, self.rect.y, 40, 40, (0, 255, 0), self)

        self.ground = Ground(0, 900, 1920, 180, (0, 0, 0))  # Adjust dimensions and color as needed

        # Gravity
        self.gravity = 0.5

        # Velocity jump
        self.jump_velocity = -10
        self.vertical_velocity = 0
        self.is_jump = False

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.square1)
        self.all_sprites.add(self.square2)
        self.all_sprites.add(self.ground)

        self.pressed = {}

    def check_collisions(self, sprite, group):
        for other_sprite in group:
            if sprite != other_sprite and pygame.sprite.collide_rect(sprite, other_sprite):
                return True
        return False

    def move_right(self, square):
        square.rect.x += self.velocity
        if self.check_collisions(square, self.all_sprites):
            square.rect.x -= self.velocity

    def move_left(self, square):
        square.rect.x -= self.velocity
        if self.check_collisions(square, self.all_sprites):
            square.rect.x += self.velocity

    def apply_gravity(self, square):
        if square.rect.y < self.ground.rect.y - square.rect.height:
            self.vertical_velocity += self.gravity
            square.rect.y += self.vertical_velocity
        else:
            self.vertical_velocity = 0
            square.rect.y = self.ground.rect.y - square.rect.height

    def handle_input(self, square):
        self.pressed = pygame.key.get_pressed()

        if self.pressed[pygame.K_d] and self.square1.rect.x + self.square1.rect.width < self.screen.get_width():
            self.move_right(self.square1)
            if self.pressed[pygame.K_SPACE]:
                self.is_jump = True
                if self.is_jump == True:
                    self.jump(self.square1)

        elif self.pressed[pygame.K_q] and self.square1.rect.x > 0:
            self.move_left(self.square1)
            if self.pressed[pygame.K_SPACE]:
                self.is_jump = True
                if self.is_jump == True:
                    self.jump(self.square1)

        elif self.pressed[pygame.K_SPACE]:
            self.is_jump = True
            if self.is_jump == True:
                self.jump(self.square1)

    def jump(self, square):
        if square.rect.y >= self.ground.rect.y - square.rect.height:
            self.vertical_velocity = self.jump_velocity
        square.rect.y += self.vertical_velocity
        self.is_jump = False


    def run(self):

        running = True

        while running:

            self.screen.blit(self.background, (0, 0))

            self.all_sprites.draw(self.screen)
            
            self.apply_gravity(self.square1)

            # Call to move the player
            self.handle_input(self.square1)

            pygame.display.flip()

            # If the player close this window
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()
