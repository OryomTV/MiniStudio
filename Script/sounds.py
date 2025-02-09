import pygame


class SoundManager:
    def __init__(self):
        self.sounds = {
            'click': pygame.mixer.Sound("Sounds/click.ogg"),
            'main': pygame.mixer.Sound("Sounds/back_music.wav"),
            'dash': pygame.mixer.Sound("Sounds/dash.wav"),
            'light': pygame.mixer.Sound("Sounds/get_light.wav"),
            'boss': pygame.mixer.Sound("Sounds/boss_music.wav")
        }
        self.volume = {
            'click': 1,
            'main': 0.1,
            'dash': 0.1,
            'light': 0.1,
            'boss': 0.1
        }

    def play(self, name):
        self.sounds[name].set_volume(self.volume.get(name, 1.0))
        self.sounds[name].play()

    def set_volume(self, name, volume):
        self.volume[name] = max(0.0, min(1.0, volume))
