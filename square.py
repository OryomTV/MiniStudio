import pygame


# Square class
class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, game):
        super().__init__()
        self.game = game

        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def square(self, surface):

        # First square
        pygame.draw.rect(surface, (0, 0, 255), self.game.square1)

        # Second square
        pygame.draw.rect(surface, (0, 255, 0), self.game.square2)
