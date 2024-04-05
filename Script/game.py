import pygame
import math

from player import Player
from player import Enemy
from ground import Ground

class Game:

    def __init__(self):

        # Create window of the game
        pygame.display.set_caption("Shining")
        self.screen = pygame.display.set_mode((1920, 1080))
        self.background = pygame.image.load("Asset/Untitled_Artwork.jpg")
        self.rect = self.background.get_rect()

        # Load button for launch the game
        self.play = pygame.image.load("Asset/bouton_jouer.png")
        self.play = pygame.transform.scale(self.play, (400, 160))
        self.play_rect = self.play.get_rect()
        self.play_rect.x = math.ceil(self.screen.get_width() / 2.5)
        self.play_rect.y = math.ceil(self.screen.get_height() / 2)

        # Load button for option 
        self.parametre = pygame.image.load("Asset/bouton_parametres.png")
        self.parametre = pygame.transform.scale(self.parametre, (380, 111))
        self.parametre_rect = self.parametre.get_rect()
        self.parametre_rect.x = math.ceil(self.screen.get_width() / 2.47)
        self.parametre_rect.y = math.ceil(self.screen.get_height() / 1.45)


        # Load button for quit the game
        self.quit = pygame.image.load("Asset/bouton_quitter.png")
        self.quit = pygame.transform.scale(self.quit, (300, 100))
        self.quit_rect = self.quit.get_rect()
        self.quit_rect.x = math.ceil(self.screen.get_width() / 2.37)
        self.quit_rect.y = math.ceil(self.screen.get_height() / 1.2)

        # Define if the game has started or not
        self.is_playing = False

        # Generate player
        self.player = Player(100, 500, "Asset/Llusern.png", 200, 160, self)
        self.enemy = Enemy(900, 450, "Asset/Pangolin.png", 150, 200, self)
        self.ground = Ground(0, 900, 1920, 180, (0, 0, 0))

        # Generate different groups
        self.all_player = pygame.sprite.Group()
        self.all_player.add(self.player)

        self.all_enemies = pygame.sprite.Group()
        self.all_enemies.add(self.enemy)

        self.all_grounds = pygame.sprite.Group()
        self.all_grounds.add(self.ground)

        # Gravity
        self.gravity = 0.5

        # Velocity jump
        self.jump_velocity = -15
        self.vertical_velocity = 0
        self.is_jump = False

        self.pressed = {}

    def start(self):
        self.is_playing = True

    def update(self):
        # Application of my player image
        self.screen.blit(self.player.image, self.player.rect)

        # Application of the monster image
        for enemy in self.all_enemies:
            self.screen.blit(enemy.image, enemy.rect)

        # Application of the set of images of my monsters group
        self.all_enemies.draw(self.screen)

        # Application of the set of images of my grounds group
        self.all_grounds.draw(self.screen)

    def apply_gravity(self):
        if self.player.position[1] < self.ground.rect.y - self.player.rect.height:
            self.vertical_velocity += self.gravity
            self.player.position[1] += self.vertical_velocity
        else:
            self.vertical_velocity = 0
            self.player.position[1] = self.ground.rect.y - self.player.rect.height

    def handle_input(self):
        self.pressed = pygame.key.get_pressed()

        if self.pressed[pygame.K_q] and self.player.rect.x > 0:
            self.player.move_left()
            if self.pressed[pygame.K_SPACE]:
                self.is_jump = True
                if self.is_jump:
                    self.jump()

        elif self.pressed[pygame.K_d] and self.player.rect.x + self.player.rect.width < self.screen.get_width():
            self.player.move_right()
            if self.pressed[pygame.K_SPACE]:
                self.is_jump = True
                if self.is_jump:
                    self.jump()

        elif self.pressed[pygame.K_SPACE] and not self.is_jump:
            self.is_jump = True
            if self.is_jump:
                self.jump()

    def jump(self):
        if self.player.position[1] >= self.ground.rect.y - self.player.rect.height:
            self.vertical_velocity = self.jump_velocity
        self.player.position[1] += self.vertical_velocity
        self.is_jump = False

    def run(self):

        clock = pygame.time.Clock()

        # boucle du jeu
        running = True

        while running:

            self.player.update()

            self.screen.blit(self.background, (0, 0))

            # Check if game has started or not
            if self.is_playing:
                # Trigger game instructions
                self.update()

            else:
                # Add welcome screen
                self.screen.blit(self.play, self.play_rect)
                self.screen.blit(self.parametre, self.parametre_rect)
                self.screen.blit(self.quit, self.quit_rect)

            self.apply_gravity()
            self.handle_input()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if mouse collides with the play button
                    if self.play_rect.collidepoint(event.pos):
                        # Launch the game
                        self.start()

                    if self.quit_rect.collidepoint(event.pos):
                        running = False

            clock.tick(120)

        pygame.quit()
