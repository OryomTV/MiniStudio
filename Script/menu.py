import sys
import pygame
import math


# LoadMenu class
class LoadMenu(pygame.sprite.Sprite):
    def __init__(self, game, menu_name, size):
        super().__init__()
        self.game = game

        self.size = size
        self.image = pygame.image.load(f'Assets/Menu/{menu_name}.png')
        self.image = pygame.transform.scale(self.image, size)


# Menu class
class Menu(LoadMenu):

    def __init__(self, game, name, size):
        super().__init__(game, name, size)
        self.game = game

        self.rect = self.image.get_rect()


# Define a class for the french play
class Play_fr(Menu):
    def __init__(self, game):
        super().__init__(game, "jouer", (400, 160))

        self.play_fr_rect = self.rect
        self.play_fr_rect.x = math.ceil(self.game.screen.get_width() / 2.7)
        self.play_fr_rect.y = math.ceil(self.game.screen.get_height() / 2)
        

class Settings_fr(Menu):
    def __init__(self, game):
        super().__init__(game, "parametres", (380, 111))

        self.sett_fr_rect = self.rect
        self.sett_fr_rect.x = math.ceil(self.game.screen.get_width() / 2.65)
        self.sett_fr_rect.y = math.ceil(self.game.screen.get_height() / 1.45)


class Quit_fr(Menu):
    def __init__(self, game):
        super().__init__(game, "quitter", (300, 100))

        self.quit_fr_rect = self.rect
        self.quit_fr_rect.x = math.ceil(self.game.screen.get_width() / 2.52)
        self.quit_fr_rect.y = math.ceil(self.game.screen.get_height() / 1.2)


class Retour(Menu):
    def __init__(self, game):
        super().__init__(game, "retour", (250, 80))

        self.retour_rect = self.rect
        self.retour_rect.x = math.ceil(self.game.screen.get_width() / 2.34)
        self.retour_rect.y = math.ceil(self.game.screen.get_height() / 1.27)


class Language_fr(Menu):
    def __init__(self, game):
        super().__init__(game, "lang_fr", (250, 80))

        self.lang_fr_rect = self.rect
        self.lang_fr_rect.x = math.ceil(self.game.screen.get_width() / 2.36)
        self.lang_fr_rect.y = math.ceil(self.game.screen.get_height() / 1.5)
        self.language = "french"


class Play_en(Menu):
    def __init__(self, game):
        super().__init__(game, "play", (400, 160))

        self.play_en_rect = self.rect
        self.play_en_rect.x = math.ceil(self.game.screen.get_width() / 2.7)
        self.play_en_rect.y = math.ceil(self.game.screen.get_height() / 2)


class Settings_en(Menu):
    def __init__(self, game):
        super().__init__(game, "settings", (380, 111))

        self.sett_en_rect = self.rect
        self.sett_en_rect.x = math.ceil(self.game.screen.get_width() / 2.65)
        self.sett_en_rect.y = math.ceil(self.game.screen.get_height() / 1.45)


class Quit_en(Menu):
    def __init__(self, game):
        super().__init__(game, "quit", (300, 100))

        self.quit_en_rect = self.rect
        self.quit_en_rect.x = math.ceil(self.game.screen.get_width() / 2.52)
        self.quit_en_rect.y = math.ceil(self.game.screen.get_height() / 1.2)


class Back(Menu):
    def __init__(self, game):
        super().__init__(game, "back", (200, 80))

        self.back_rect = self.rect
        self.back_rect.x = math.ceil(self.game.screen.get_width() / 2.28)
        self.back_rect.y = math.ceil(self.game.screen.get_height() / 1.27)


class Language_en(Menu):
    def __init__(self, game):
        super().__init__(game, "lang_en", (250, 80))

        self.lang_en_rect = self.rect
        self.lang_en_rect.x = math.ceil(self.game.screen.get_width() / 2.36)
        self.lang_en_rect.y = math.ceil(self.game.screen.get_height() / 1.5)
        self.language = "english"

class CreateMenu:
    def __init__(self, game):
        self.game = game

        # Current screen
        self.current_screen = "main_fr"

        # Menus
        self.main_fr_menus = pygame.sprite.Group()
        self.settings_fr_menus = pygame.sprite.Group()
        self.main_en_menus = pygame.sprite.Group()
        self.settings_en_menus = pygame.sprite.Group()

        # Generate menus
        self.create_menus()

    def create_menus(self):
        # Main french menus
        self.play_fr = Play_fr(self.game)
        self.quit_fr = Quit_fr(self.game)
        self.settings_fr = Settings_fr(self.game)
        self.main_fr_menus.add(self.play_fr, self.quit_fr, self.settings_fr)

        # Settings french menus
        self.retour = Retour(self.game)
        self.lang_fr = Language_fr(self.game)
        self.settings_fr_menus.add(self.retour, self.lang_fr)

        # Main english menus
        self.play_en = Play_en(self.game)
        self.quit_en = Quit_en(self.game)
        self.settings_en = Settings_en(self.game)
        self.main_en_menus.add(self.play_en, self.quit_en, self.settings_en)

        # Settings english menus
        self.back = Back(self.game)
        self.lang_en = Language_en(self.game)
        self.settings_en_menus.add(self.back, self.lang_en)

    def load_different_screens(self):
        if self.current_screen == "main_fr":
            self.game.screen.blit(self.game.background, (0, 0))
            self.main_fr_menus.draw(self.game.screen)

        elif self.current_screen == "settings_fr":
            self.game.screen.blit(self.game.background_2, (0, 0))
            self.settings_fr_menus.draw(self.game.screen)

        elif self.current_screen == "main_en":
            self.game.screen.blit(self.game.background, (0, 0))
            self.main_en_menus.draw(self.game.screen)

        elif self.current_screen == "settings_en":
            self.game.screen.blit(self.game.background_3, (0, 0))
            self.settings_en_menus.draw(self.game.screen)

        elif self.current_screen == "play_fr" or self.current_screen == "play_en":
            self.game.screen.blit(self.game.background, (0, 0))
            self.game.draw()
            #self.game.transparent_cube()

        elif self.current_screen == "level_2":
            self.game.screen.blit(self.game.background_4, (0, 0))
            self.game.draw()

    def choice_menus(self, event):
        if self.current_screen == "main_fr":
            # If play is clicked
            if self.play_fr.play_fr_rect.collidepoint(event.pos):
                self.current_screen = "play_fr"
                self.game.is_playing = True
                self.game.tilemap.render(self.game.background)

                if self.game.is_playing:
                    # Play sound
                    self.game.sound_manager.play('click')

                if event.type == pygame.KEYDOWN and event.key == pygame.K_b and self.game.is_playing:
                    self.current_screen = "main_fr"

            # If settings button is clicked
            elif self.settings_fr.sett_fr_rect.collidepoint(event.pos):
                self.current_screen = "settings_fr"
                self.game.sound_manager.play('click')

            # If quit is clicked
            elif self.quit_fr.quit_fr_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

        elif self.current_screen == "settings_fr":
            # If retour is clicked
            if self.retour.retour_rect.collidepoint(event.pos):
                self.current_screen = "main_fr"

            # If language is clicked
            elif self.lang_fr.lang_fr_rect.collidepoint(event.pos):
                self.current_screen = "settings_en"

        elif self.current_screen == "main_en":
            # If play is clicked
            if self.play_en.play_en_rect.collidepoint(event.pos):
                self.current_screen = "play_en"
                self.game.is_playing = True
                self.game.tilemap.render(self.game.background)

                if self.game.is_playing:
                    # Play sound
                    self.game.sound_manager.play('click')

                if event.type == pygame.KEYDOWN and event.key == pygame.K_b and self.game.is_playing:
                    self.current_screen = "main_en"

            # If settings button is clicked
            elif self.settings_en.sett_en_rect.collidepoint(event.pos):
                self.current_screen = "settings_en"
                self.game.sound_manager.play('click')

            # If quit is clicked
            elif self.quit_en.quit_en_rect.collidepoint(event.pos):
                pygame.quit()

        elif self.current_screen == "settings_en":
            # If retour is clicked
            if self.back.back_rect.collidepoint(event.pos):
                self.current_screen = "main_en"

            # If language is clicked
            elif self.lang_en.lang_en_rect.collidepoint(event.pos):
                self.current_screen = "settings_fr"
