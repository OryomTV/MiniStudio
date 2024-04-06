import pygame
import math

from player import Player
from player import Enemy
from ground import Ground
from obscurity import Obscurity
from sounds import SoundManager
from menu import Menu, Play_fr, Quit_fr, Settings_fr, Retour, Language_fr, Play_en, Settings_en, Quit_en, Back, Language_en


class Game:

    def __init__(self):

        # Create window of the game
        pygame.display.set_caption("Shining")
        self.screen = pygame.display.set_mode((1920, 1080))
        self.background = pygame.image.load("assets/Kingdom Hearts 3_2.jpg")
        self.background_2 = pygame.image.load("assets/settings_french.jpg")
        self.background_3 = pygame.image.load("assets/settings_english.jpg")
        self.rect = self.background.get_rect()

        # Define the game has started
        self.is_playing = False

        # Generate player
        self.player = Player(100, 500, "assets/player.png", 200, 160, self)
        self.enemy = Enemy(900, 450, "assets/mummy.png", 150, 200, self)
        self.ground = Ground(0, 900, 1920, 180, (0, 0, 0))

        # Generate menus
        self.play_fr = Play_fr(self)
        self.quit_fr = Quit_fr(self)
        self.settings_fr = Settings_fr(self)
        self.retour = Retour(self)
        self.lang_fr = Language_fr(self)

        self.play_en = Play_en(self)
        self.settings_en = Settings_en(self)
        self.quit_en = Quit_en(self)
        self.back = Back(self)
        self.lang_en = Language_en(self)

        # Generate obscurity
        self.obscurity = Obscurity((1920, 1080))

        # Generate different groups
        self.all_player = pygame.sprite.Group()
        self.all_player.add(self.player)

        self.all_enemies = pygame.sprite.Group()
        self.all_enemies.add(self.enemy)

        self.all_grounds = pygame.sprite.Group()
        self.all_grounds.add(self.ground)

        self.all_menus = pygame.sprite.Group()

        # Gravity
        self.gravity = 0.5

        # Velocity jump
        self.jump_velocity = -15
        self.vertical_velocity = 0
        self.is_jump = False

        self.pressed = {}

        # Manage sounds
        self.sound_manager = SoundManager()

        # Menus
        self.main_fr_menus = pygame.sprite.Group()
        self.settings_fr_menus = pygame.sprite.Group()
        self.main_en_menus = pygame.sprite.Group()
        self.settings_en_menus = pygame.sprite.Group()

        # Create menus
        self.create_menus()

        # Current screen
        self.current_screen = "main_fr"

    def create_menus(self):
        # Main french menus
        self.play_fr = Play_fr(self)
        self.quit_fr = Quit_fr(self)
        self.settings_fr = Settings_fr(self)
        self.main_fr_menus.add(self.play_fr, self.quit_fr, self.settings_fr)

        # Settings french menus
        self.retour = Retour(self)
        self.lang_fr = Language_fr(self)
        self.settings_fr_menus.add(self.retour, self.lang_fr)

        # Main english menus
        self.play_en = Play_en(self)
        self.quit_en = Quit_en(self)
        self.settings_en = Settings_en(self)
        self.main_en_menus.add(self.play_en, self.quit_en, self.settings_en)

        # Settings english menus
        self.back = Back(self)
        self.lang_en = Language_en(self)
        self.settings_en_menus.add(self.back, self.lang_en)

    def choice_menus(self, event):
        if self.current_screen == "main_fr":
            # If play is clicked
            if self.play_fr.rect.collidepoint(event.pos):
                self.current_screen = "play_fr"
                self.is_playing = True

                if self.is_playing:
                    # Play sound
                    self.sound_manager.play('click')

                if event.type == pygame.KEYDOWN and event.key == pygame.K_b and self.is_playing:
                    self.current_screen = "main_fr"

            # If settings button is clicked
            elif self.settings_fr.rect.collidepoint(event.pos):
                self.current_screen = "settings_fr"

            # If quit is clicked
            elif self.quit_fr.rect.collidepoint(event.pos):
                pygame.quit()

        elif self.current_screen == "settings_fr":
            # If retour is clicked
            if self.retour.rect.collidepoint(event.pos):
                self.current_screen = "main_fr"

            # If language is clicked
            elif self.lang_fr.rect.collidepoint(event.pos):
                self.current_screen = "settings_en"

        elif self.current_screen == "main_en":
            # If play is clicked
            if self.play_en.rect.collidepoint(event.pos):
                self.current_screen = "play_en"
                self.is_playing = True

                if self.is_playing:
                    # Play sound
                    self.sound_manager.play('click')

                if event.type == pygame.KEYDOWN and event.key == pygame.K_b and self.is_playing:
                    self.current_screen = "main_en"

            # If settings button is clicked
            elif self.settings_en.rect.collidepoint(event.pos):
                self.current_screen = "settings_en"

            # If quit is clicked
            elif self.quit_en.rect.collidepoint(event.pos):
                pygame.quit()

        elif self.current_screen == "settings_en":
            # If retour is clicked
            if self.back.rect.collidepoint(event.pos):
                self.current_screen = "main_en"

            # If language is clicked
            elif self.lang_en.rect.collidepoint(event.pos):
                self.current_screen = "settings_fr"

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

        # Apply the obscurity one the player
        self.obscurity.shadow(self.screen, 400, 100, self.player.rect.center)

        self.apply_gravity()
        self.handle_input()

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

            if self.current_screen == "main_fr":
                self.screen.blit(self.background, (0, 0))
                self.main_fr_menus.draw(self.screen)

            elif self.current_screen == "settings_fr":
                self.screen.blit(self.background_2, (0, 0))
                self.settings_fr_menus.draw(self.screen)

            elif self.current_screen == "main_en":
                self.screen.blit(self.background, (0, 0))
                self.main_en_menus.draw(self.screen)

            elif self.current_screen == "settings_en":
                self.screen.blit(self.background_3, (0, 0))
                self.settings_en_menus.draw(self.screen)

            elif self.current_screen == "play_fr":
                self.screen.blit(self.background, (0, 0))
                self.update()

            elif self.current_screen == "play_en":
                self.screen.blit(self.background, (0, 0))
                self.update()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.choice_menus(event)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b and self.is_playing:
                        self.current_screen = "main_fr" if self.current_screen == "play_fr" else "main_en"

            clock.tick(120)

        pygame.quit()
