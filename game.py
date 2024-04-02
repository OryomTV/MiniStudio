import pygame
from square import Square


# Game class
class Game:

    def __init__(self):

        # Create window
        pygame.display.set_caption("Shining")
        self.screen = pygame.display.set_mode((1920, 1080))
        self.background = pygame.image.load("assets/Kingdom Hearts 3_2.jpg")

        # Square information
        self.rect = self.background.get_rect()
        self.rect.x = 600
        self.rect.y = 700
        self.velocity = 1

        self.square1 = Square(self.rect.x, self.rect.y, 30, 30, (0, 0, 255), self)
        self.square2 = Square(self.rect.x + 250, self.rect.y, 40, 40, (0, 255, 0), self)

        # Generation of player
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.square1)
        self.all_sprites.add(self.square2)

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

    def move_up(self, square):
        square.rect.y -= self.velocity
        if self.check_collisions(square, self.all_sprites):
            square.rect.y += self.velocity

    def move_down(self, square):
        square.rect.y += self.velocity
        if self.check_collisions(square, self.all_sprites):
            square.rect.y -= self.velocity

    def handle_input(self, square):
        self.pressed = pygame.key.get_pressed()

        # Check where player want to go
        if self.pressed[pygame.K_d] and self.square1.rect.x + self.square1.rect.width < self.screen.get_width():
            self.move_right(self.square1)

        elif self.pressed[pygame.K_q] and self.square1.rect.x > 0:
            self.move_left(self.square1)

        elif self.pressed[pygame.K_z] and self.square1.rect.y > 0:
            self.move_up(self.square1)

        elif self.pressed[pygame.K_s] and self.square1.rect.y + self.square1.rect.height < self.screen.get_height():
            self.move_down(self.square1)

    def run(self):

        # Playing loop
        running = True

        while running:

            # Application of the background
            self.screen.blit(self.background, (0, 0))

            self.all_sprites.draw(self.screen)

            # Call to move the player
            self.handle_input(self.square1)

            pygame.display.flip()

            # If the player close this window
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()
