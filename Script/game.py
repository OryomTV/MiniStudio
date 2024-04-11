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
        self.background = pygame.image.load("Assets/Background/tuto.png").convert()
        self.background_2 = pygame.image.load("Assets/Menu/settings_french.jpg").convert()
        self.background_3 = pygame.image.load("Assets/Menu/settings_english.jpg").convert()
        self.background_4 = pygame.image.load("Assets/Background/level_2.jpg").convert()
        self.background_4 = pygame.transform.scale(self.background_4, (1920, 1080))
        self.rect = self.background.get_rect()

        self.display = pygame.Surface((1920, 1080))
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
            'decoration': load_images('tiles/decoration', size=(64, 64))
        }

        # Generate player
        self.player = Player(self, (800, 120), 'Assets/Entities/Llursen.png', 80, 100)
        
        self.enemy = Enemy(self, (900, 450), "Assets/Entities/Bat.png", 150, 200, "Tatoo",(1, 0), 100)
        
        self.ground = Ground(0, 900, 1920, 180, (0, 0, 0))
        
        self.plateforme = Plateforme(900, 600, 600, 400, "Assets/Tuto/tiles/platform/platform1_tuto.png", True, (-1, 1), 100)
        self.plateformes_rect_rect = [self.plateforme.rect]
        self.menu = CreateMenu(self)

        self.tilemap = Tilemap(self, tile_size=64)
        self.tilemap.load("Script/map.json")

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

        # Velocity jump

        self.player_should_jump = False

        self.pressed = {}

        self.movement = 0

        self.delta_time = 0.0

        # Dash

        self.player_should_dash = False
        self.dash_direction = False
        
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
        self.player.position = [100, 500]
        self.menu.current_screen = "main_fr"

    def draw(self):
        # Application of my player image
        self.player.draw(self.screen)

        # Application of the monster image
        for enemy in self.all_enemies:
            if self.enemy.Alive:
                self.screen.blit(enemy.image, enemy.rect)

        self.plateforme.draw(self.screen)
        # Application of the set of images of my monsters group
        #self.all_enemies.draw(self.screen)

        # Application of the set of images of my grounds group
        #self.all_grounds.draw(self.screen)

        # Application of the set of images of our platforms group
        #self.all_plateforme.draw(self.screen)

        # Apply the obscurity one the player
        #self.obscurity.shadow(self.screen, 400, 100, self.player.rect.center)
        

    def update(self):
        self.plateforme.move(1)
        self.player.Update(self.tilemap, self.movement, self.player_should_jump, self.player_should_dash, self.dash_direction, self.delta_time, self.plateformes_rect_rect)
        self.enemy.move(1)
        for enemy in self.all_enemies:
            if self.enemy.Alive and self.player.rect.colliderect(enemy.rect):
                if self.player.onDash:
                    self.enemy.Alive = False
                else:
                    self.game_over()
                    for enemy in self.all_enemies:
                        self.enemy.Alive = True
                    


    def handle_input(self):
        self.pressed = pygame.key.get_pressed()
        self.movement = self.pressed[pygame.K_d] - self.pressed[pygame.K_q]
        self.player_should_jump = self.pressed[pygame.K_SPACE]
        self.player_should_dash = self.pressed[pygame.K_c]
        self.dash_direction = self.pressed[pygame.K_q]

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

            self.delta_time = clock.tick(60) / 1000.0

        pygame.quit()
        sys.exit()
