import pygame, os
from pytmx.util_pygame import load_pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Tree
from support import *

class Level:
    def __init__(self):
        # get the dislay surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()

        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):

        tmx_data = load_pygame(os.path.join(os.path.dirname(__file__), '..', 'data', 'tmx', 'world.tmx'))
        boundary = import_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'FloorBlocks.csv'))

        for layer in ['grass', 'dirt', 'bridge', 'platform']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS['ground'])

        for x, y, surf in tmx_data.get_layer_by_name('water').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS['water'])
        
        for x, y, surf in tmx_data.get_layer_by_name('FloorBlocks').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.collision_sprites, LAYERS['grass'])

        for object in ['trees']:
            for obj in tmx_data.get_layer_by_name(object):
                Tree(
                    (obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites]
                )
        for obj in tmx_data.get_layer_by_name('entities'):
            self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)

        self.overlay.display()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # zoom
        self.zoom_scale = 1
        self.internal_surface_size = (2500, 2500)
        self.internal_surface = pygame.Surface(self.internal_surface_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surface.get_rect(center = (self.half_w, self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surface_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surface_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surface_size[1] // 2 - self.half_h

    def keyboard_zoom(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q] and self.zoom_scale <= 2:
            self.zoom_scale += 0.1
        if keys[pygame.K_e] and self.zoom_scale >= 0.7:
            self.zoom_scale -= 0.1

    def custom_draw(self, player):

        self.offset.x = player.rect.centerx - SCREEN_WIDTH // 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT // 2

        self.internal_surface.fill('black')
        self.keyboard_zoom()

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
                    self.internal_surface.blit(sprite.image, offset_pos)
                    # offset_rect = sprite.rect.copy()
                    # offset_rect.center -= self.offset
                    # self.display_surface.blit(sprite.image, offset_rect)
        
        scaled_surface = pygame.transform.scale(self.internal_surface, self.internal_surface_size_vector * self.zoom_scale)
        scaled_rect = scaled_surface.get_rect(center = (self.half_w, self.half_h))

        self.display_surface.blit(scaled_surface, scaled_rect)



