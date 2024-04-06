import pygame


class Obscurity:
    def __init__(self, surface_size):
        self.surface_size = surface_size
        self.dark_filter = pygame.Surface(surface_size, pygame.SRCALPHA)
        self.dark_filter.fill((0, 0, 0, 1))
        self.object_filter = pygame.Surface(surface_size, pygame.SRCALPHA)

    def shadow(self, surface, transparent, radius, obj_center):
        surface.blit(self.dark_filter, (0, 0))

        if obj_center is not None:
            self.object_filter.fill((0, 0, 0, transparent // 2))
            pygame.draw.circle(self.object_filter, (0, 0, 0, 0), obj_center, radius)
            surface.blit(self.object_filter, (0, 0))
        else:
            dark_filter = pygame.Surface(self.surface_size, pygame.SRCALPHA)
            dark_filter.fill((0, 0, 0, transparent))
            surface.blit(dark_filter, (0, 0))
