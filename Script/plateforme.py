import pygame


class Plateforme(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path, view, direction, max_distance):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction_X = direction[0]
        self.direction_Y = direction[1]
        self.max_distance = max_distance
        self.distance_moved = 0
        self.view = view

    def move(self, speed):

        self.rect.x += speed * self.direction_X
        self.rect.y += speed * self.direction_Y

        if self.max_distance is not None:
            self.distance_moved += speed

        if self.max_distance is not None and self.distance_moved >= self.max_distance:
            self.direction_X *= -1
            self.direction_Y *= -1
            self.distance_moved = 0

    def draw(self, surface):
        if self.view:
            # Load image
            surface.blit(self.image, self.rect)
