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
from Constants import *

class Game:

    def __init__(self):

        # Create window of the game
        pygame.display.set_caption("Shining")
        self.screen = pygame.display.set_mode((1920, 1080))
        self.background = pygame.image.load("../Assets/Background/tuto.png").convert()
        self.background_2 = pygame.image.load("../Assets/Menu/settings_french.jpg").convert()
        self.background_3 = pygame.image.load("../Assets/Menu/settings_english.jpg").convert()
        self.background_4 = pygame.image.load("../Assets/Background/level_2.png").convert()
        self.background_4 = pygame.transform.scale(self.background_4, (1920, 1080))
        self.rect = self.background.get_rect()

        self.display = pygame.Surface((500, 500))
        # Define the game has started
        self.is_playing = False

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
            'player': load_images('tiles/recess/normal'),
            'decoration': load_images('tiles/decoration', size=(64, 64)),
            'cathedral': load_images('tiles/cathedral', size=(64, 64)),
            'pillar': load_images('tiles/pillar', size=(100, 250)),
            'ground_floor': load_images('tiles/ground_floor', size=(64, 64))
        }


        # Generate player
        self.player = Player(self, (250, 900), 80, 80)

        self.enemy = Enemy(self, (900, 450), "../Assets/Entities/Bat.png", 150, 200, "Bat",(1, 1), 100)

        self.ground = Ground(0, 900, 1920, 180, (0, 0, 0))

        self.plateforme = Plateforme(735, 840, 130, 25, "../Assets/Tuto/tiles/platform/platform1_tuto.png", True, (-1, 1), 100)
        self.plateforme_2 = Plateforme(840, 692, 130, 25, "../Assets/Tuto/tiles/platform/platform1_tuto.png", True, (-1, 1), 100)
        self.plateforme_3 = Plateforme(669, 555, 130, 25, "../Assets/Tuto/tiles/platform/platform1_tuto.png", True, (-1, 1), 100)
        self.plateforme_4 = Plateforme(359, 448, 130, 25, "../Assets/Tuto/tiles/platform/platform1_tuto.png", True, (-1, 1), 100)
        self.plateforme_5 = Plateforme(417, 280, 130, 25, "../Assets/Tuto/tiles/platform/platform1_tuto.png", True, (-1, 1), 100)
        
        self.plateformes_rect_rect = [self.plateforme.rect, self.plateforme_2.rect, self.plateforme_3.rect, self.plateforme_4.rect, self.plateforme_5.rect]

        self.menu = CreateMenu(self)

        self.tilemap = Tilemap(self, tile_size=64)
        self.tilemap.load("map.json")

        self.tilemap2 = Tilemap(self, tile_size=64)
        self.tilemap2.load("map2.json")

        self.tilemap3 = Tilemap(self, tile_size=64)
        self.tilemap3.load("map3.json")

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

        self.plateformes = pygame.sprite.Group()
        self.plateformes.add(self.plateforme, self.plateforme_2, self.plateforme_3, self.plateforme_4, self.plateforme_5)

        self.all_menus = pygame.sprite.Group()

        # Velocity jump

        self.player_should_jump = False

        self.pressed = {}

        self.movement = 0

        self.delta_time = 0

        # Manage sounds
        self.sound_manager = SoundManager()

        # Create menus
        self.menu.create_menus()

        # Cube for pass to level 2
        self.cube = pygame.Rect(1700, 700, 100, 100)
        self.transparent_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.rect(self.transparent_surface, (0, 0, 0, 0), self.transparent_surface.get_rect())

        # Cube for pass to level 3
        self.cube2 = pygame.Rect(1000, 700, 100, 100)
        self.transparent_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.rect(self.transparent_surface, (0, 0, 0, 0), self.transparent_surface.get_rect())

    def transparent_cube(self):
        # Check if player and cube collides
        if self.player.rect.colliderect(self.cube):
            self.menu.current_screen = "level_2"
            self.tilemap2.render(self.background_4)
            self.player.position = [100, 100]  # Change les valeurs en fonction de là ou tu veux que le joueur soit (t'es pas con je le sais mais je dis quand même)

        elif self.player.rect.colliderect(self.cube2):
            self.menu.current_screen = "level_3"
            self.tilemap3.render(self.background_4)
            self.player.position = [100, 100]

        # J'ai pas testé si c'était bon parce que j'ai plus le perso mais normalement ça devrait être bon
        # Et du coup pour faire les zones où on meurt dans le vide t'as juste à créer des zones de collisions et que tu meurs dedans genre
        if self.menu.current_screen == "play_fr" or self.menu.current_screen == "play_en":
            self.screen.blit(self.transparent_surface, self.cube)
        elif self.menu.current_screen == "level_2":
            self.screen.blit(self.transparent_surface, self.cube2)

    def game_over(self):
        # Reload the game
        self.all_enemies = pygame.sprite.Group()
        self.player.health = self.player.maxHealth
        self.player.position = [100, 500]
        self.menu.current_screen = "main_fr"

    def draw(self):

        # Application of the set of images of our platforms group
        for plateforme in self.plateformes:
            plateforme.draw(self.screen)

        # Application of my player image
        self.player.draw(self.screen)

        # Application of the monster image
        for enemy in self.all_enemies:
            self.screen.blit(enemy.image, enemy.rect)

        # Application of the set of images of my monsters group
        self.all_enemies.draw(self.screen)

        # Apply the obscurity one the player
        self.obscurity.shadow(self.screen, 400, 100, self.player.rect.center)

    def update(self):
        #self.player.Update(self.tilemap, self.movement, self.player_should_jump, self.delta_time, self.plateformes_rect_rect)
        self.enemy.move(1)

    def handle_input(self):
        self.pressed = pygame.key.get_pressed()
        self.movement = self.pressed[pygame.K_d] - self.pressed[pygame.K_q]
        self.player_should_jump = self.pressed[pygame.K_SPACE]

    def run(self):

        clock = pygame.time.Clock()

        # boucle du jeu
        running = True
        sound_playing = False

        while running:

            if not sound_playing:
                self.sound_manager.play('main')
                sound_playing = True

            self.handle_input()
            self.update()

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

            self.delta_time = clock.tick(60) / 1000

        pygame.quit()
        sys.exit()
