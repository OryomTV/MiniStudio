import pygame
import math


# LoadMenu class
class LoadMenu(pygame.sprite.Sprite):
    def __init__(self, menu_name, size):
        super().__init__()

        self.size = size
        self.image = pygame.image.load(f'Assets/{menu_name}.png')
        self.image = pygame.transform.scale(self.image, size)


# Menu class
class Menu(LoadMenu):

    def __init__(self, game, name, size):
        super().__init__(name, size)
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
        self.retour_rect.x = math.ceil(self.game.screen.get_width() / 2.36)
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
        super().__init__(game, "back", (250, 80))

        self.back_rect = self.rect
        self.back_rect.x = math.ceil(self.game.screen.get_width() / 2.36)
        self.back_rect.y = math.ceil(self.game.screen.get_height() / 1.27)


class Language_en(Menu):
    def __init__(self, game):
        super().__init__(game, "lang_en", (250, 80))

        self.lang_en_rect = self.rect
        self.lang_en_rect.x = math.ceil(self.game.screen.get_width() / 2.36)
        self.lang_en_rect.y = math.ceil(self.game.screen.get_height() / 1.5)
        self.language = "english"

