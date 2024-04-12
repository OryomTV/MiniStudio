import sys
import pygame

from utils import load_images
from tilemap import Tilemap

RENDER_SCALE = 1.0


class Editor:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('editor')
        self.screen = pygame.display.set_mode((1920, 1080))
        self.display = pygame.Surface((1920, 1080))

        self.clock = pygame.time.Clock()

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
            'cathedral': load_images('tiles/cathedral', size=(64, 64)),
            'decoration': load_images('tiles/decoration', size=(64, 64)),
            'pillar': load_images('tiles/pillar', size=(100, 250)),
            'ground_floor': load_images('tiles/ground_floor', size=(64, 64))
        }

        self.movement = [False, False, False, False]

        self.tilemap = Tilemap(self, tile_size=64)

        try:
            #pass
            self.tilemap.load('Script/map2.json')
        except FileNotFoundError:
            pass

        self.scroll = [0, 0]

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True

    def run(self):
        while True:
            self.display.fill((0, 0, 0))

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2

            render_scroll = (int(self.scroll[0] * RENDER_SCALE), int(self.scroll[1] * RENDER_SCALE))

            self.tilemap.render(self.display, offset=render_scroll)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(250)

            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE - render_scroll[0], mpos[1] / RENDER_SCALE - render_scroll[1])

            tile_pos = (int((mpos[0]) // self.tilemap.tile_size),
                        int((mpos[1]) // self.tilemap.tile_size))

            if self.ongrid:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0],
                                                     tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_img, mpos)

            if self.clicking and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {
                    'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1],
                                         tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)

            self.display.blit(current_tile_img, (5, 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append(
                                {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant,
                                 'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(
                                self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(
                                self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.movement[0] = True
                    if event.key == pygame.K_q:
                        self.movement[1] = True
                    if event.key == pygame.K_s:
                        self.movement[2] = True
                    if event.key == pygame.K_z:
                        self.movement[3] = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_o:
                        self.tilemap.save('map2.json')
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.movement[0] = False
                    if event.key == pygame.K_q:
                        self.movement[1] = False
                    if event.key == pygame.K_s:
                        self.movement[2] = False
                    if event.key == pygame.K_z:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


Editor().run()
