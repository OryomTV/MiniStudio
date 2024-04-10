import sys
import pygame
import math

from entity import Player
from entity import Enemy
from ground import Ground
from plateforme import Plateforme
from obscurity import Obscurity
from sounds import SoundManager
from menu import *
from tilemap import Tilemap
from utils import load_images, load_image


class Game:

    def __init__(self):

        # Create window of the game
        pygame.display.set_caption("Shining")
        self.screen = pygame.display.set_mode((1920, 1080))
        self.background = pygame.image.load("../Assets/Background/tuto.png").convert()
        self.background_2 = pygame.image.load("../Assets/Menu/settings_french.jpg").convert()
        self.background_3 = pygame.image.load("../Assets/Menu/settings_english.jpg").convert()
        self.background_4 = pygame.image.load("../Assets/Background/level_2.jpg").convert()
        self.background_4 = pygame.transform.scale(self.background_4, (1920, 1080))
        self.rect = self.background.get_rect()

        # Define the game has started
        self.is_playing = False

        # Generate player

        self.player = Player(self, 100, 500, "../Assets/Entities/player.png", 120, 100)
        self.enemy = Enemy(self, 900, 450, "../Assets/Entities/mummy.png", 150, 200, (1, 0), 100)
        self.ground = Ground(0, 900, 1920, 180, (0, 0, 0))
        self.plateforme = Plateforme(900, 600, 600, 400, "../Assets/Tuto/tiles/platform/platform1_tuto.png", True, (-1, 1), 100)
        self.menu = CreateMenu(self)

        # Generate assets
        self.assets = {
            'corner_alternative': load_images('tiles/corner/alternatif', size=(64, 64)),
            'corner_normal': load_images('tiles/corner/normal', size=(64, 64)),
            'flat_corner_alternative': load_images('tiles/flat_corner/alternatif', size=(64, 64)),
            'flat_corner_normal': load_images('tiles/flat_corner/normal', size=(64, 64)),
            'flat_ground_normal': load_images('tiles/flat_ground/normal', size=(64, 64)),
            'flat_recess_alternative': load_images('tiles/flat_recess/alternatif', size=(64, 64)),
            'flat_recess_normal': load_images('tiles/flat_recess/normal', size=(64, 64)),
            'ground_alternative': load_images('tiles/ground/alternatif', size=(64, 64)),
            'ground_normal': load_images('tiles/ground/normal', size=(64, 64)),
            'platform': load_images('tiles/platform', size=(250, 250)),
            'recess_alternative': load_images('tiles/recess/alternatif', size=(64, 64)),
            'recess_normal': load_images('tiles/recess/normal', size=(64, 64)),
        }

        self.tilemap = Tilemap(self, tile_size=64)
        self.tilemap.load('map.json')

        self.scroll = [0, 0]

        # Generate obscurity
        self.obscurity = Obscurity((1920, 1080))

        # Generate different groups
        self.all_player = pygame.sprite.Group()
        self.all_player.add(self.player)

        self.all_enemies = pygame.sprite.Group()
        self.all_enemies.add(self.enemy)

        self.all_grounds = pygame.sprite.Group()
        self.all_grounds.add(self.ground)

        self.all_plateforme = pygame.sprite.Group()
        self.all_plateforme.add(self.plateforme)

        self.all_menus = pygame.sprite.Group()

        # Gravity
        self.gravity = 0.5

        # Velocity jump
        self.jump_velocity = -10
        self.vertical_velocity = 0
        self.is_jump = False

        self.pressed = {}

        # Manage sounds
        self.sound_manager = SoundManager()

        # Create menus
        self.menu.create_menus()

        # Creation of the transparent surface and rectangle transparent
        self.cube = pygame.Rect(1700, 700, 100, 100)
        self.transparent_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.rect(self.transparent_surface, (0, 0, 0, 0), self.transparent_surface.get_rect())

    def transparent_cube(self):
        # Check if player and cube collides
        if self.player.rect.colliderect(self.cube):
            self.menu.current_screen = "level_2"
            self.player.position = [100, 100]

        self.screen.blit(self.transparent_surface, self.cube)

    def game_over(self):
        # Reload the game
        self.all_enemies = pygame.sprite.Group()
        self.player.health = self.player.maxHealth
        self.player.position = [100, 500]
        self.menu.current_screen = "main_fr"

    def update(self):
        # Application of my player image
        self.screen.blit(self.player.image, self.player.rect)

        # Application of the monster image
        #for enemy in self.all_enemies:
            #self.screen.blit(enemy.image, enemy.rect)

        # Application of the set of images of my monsters group
        #self.all_enemies.draw(self.screen)

        # Application of the set of images of my grounds group
        #self.all_grounds.draw(self.screen)

        # Application of the set of images of our platforms group
        #self.all_plateforme.draw(self.screen)

        # Apply the obscurity one the player
        #self.obscurity.shadow(self.screen, 400, 100, self.player.rect.center)

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
        sound_playing = False

        while running:

            if not sound_playing:
                self.sound_manager.play('main')
                sound_playing = True

            self.player.update()

            self.plateforme.move(1)

            self.enemy.move(1)

            self.menu.load_different_screens()

            # Check if sound is already play
            if not pygame.mixer.get_busy():
                sound_playing = False

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.menu.choice_menus(event)

                elif event.type == pygame.KEYDOWN:
                    if self.is_playing:
                        if event.key == pygame.K_ESCAPE:
                            self.menu.current_screen = "main_fr" if self.menu.current_screen == "play_fr" else "main_en"
                            self.is_playing = False

            clock.tick(120)

        pygame.quit()
        sys.exit()
