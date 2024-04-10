import pygame


class Entity(pygame.sprite.Sprite):

    def __init__(self, x, y, game):
        super().__init__()
        self.game = game

        self.position = [x, y]
        self.velocity = 2.5

        self.old_position = self.position.copy()

    def check_collisions(self, sprite, group):
        for other_sprite in group:
            if sprite != other_sprite and pygame.sprite.collide_rect(sprite, other_sprite):
                return True
        return False

    def move_right(self):
        self.position[0] += self.velocity
        if self.check_collisions(self, self.game.all_grounds):
            self.position[0] -= self.velocity
        self.image = pygame.transform.flip(self.original_image, False, False)

    def move_left(self):
        self.position[0] -= self.velocity
        if self.check_collisions(self, self.game.all_grounds):
            self.position[0] += self.velocity
        self.image = pygame.transform.flip(self.original_image, True, False)

    def update(self):
        self.rect.topleft = self.position


class Player(Entity):

    def __init__(self, game, x, y, image_path, width, height):
        super().__init__(x, y, game)

        # Information about player
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.original_image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

    def draw(self, surface):
        # Load image
        surface.blit(self.image, self.rect)


class Enemy(Entity):

    def __init__(self, game, x, y, image_path, width, height, direction, max_distance):
        super().__init__(x, y, game)

        # Information about enemy
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.distance_moved = 0
        self.direction_X = direction[0]
        self.direction_Y = 0
        self.max_distance = max_distance

    def move(self, speed):

        self.rect.x += speed * self.direction_X

        if self.max_distance is not None:
            self.distance_moved += speed

        if self.max_distance is not None and self.distance_moved >= self.max_distance:
            self.direction_X *= -1
            self.distance_moved = 0

    def draw(self, surface):
        # Draw the enemy on the surface
        surface.blit(self.image, self.rect)
