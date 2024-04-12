import pygame

# class MyRect(pygame.Rect):
#     def __init__(self, rect):
#         super().__init__(rect)
#         self.childingMethod = None

class Plateforme(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path, view, direction, max_distance):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction_X = direction[0]
        self.direction_Y = direction[1]
        self.max_distance = max_distance
        self.distance_moved = 0
        self.view = view
        self.debugSurf = pygame.Surface((width, height))
        self.debugSurf.fill((255, 0, 0))
        self.debugSurf.set_colorkey((255, 0, 0))
        self.collided_player = None
        self.max_distance_to_child = 90000

    def move(self, speed):

        self.rect.x += speed * self.direction_X
        self.rect.y += speed * self.direction_Y

        if self.max_distance is not None:
            self.distance_moved += speed

        if self.max_distance is not None and self.distance_moved >= self.max_distance:
            self.direction_X *= -1
            self.direction_Y *= -1
            self.distance_moved = 0
    
        # if self.collided_player is not None:
        #     self.collided_player.rect.x += speed * self.direction_X
        #     self.collided_player.rect.y += speed * self.direction_Y
        #     # dx = abs(self.collided_player.rect.centerx - self.rect.x)
        #     # dy = abs(self.collided_player.rect.y - self.rect.y)
        #     # if (dx * dx + dy * dy) > self.max_distance_to_child:
        #     if not self.collided_player.bigger_rect.colliderect(self.rect):
        #         print("unchilded")
        #         self.collided_player = None

    # def make_player_a_child(self, player):
    #     print("childed")
    #     self.collided_player = player
        
    def draw(self, surface):
        if self.view:
            # Load image
            surface.blit(self.debugSurf, self.rect)