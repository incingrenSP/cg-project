import pygame, os
from pytmx.util_pygame import load_pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, Decors, Tree
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

        # tmx_data = load_pygame(os.path.join(os.path.dirname(__file__), '..', 'data', 'world.tmx'))

        # for layer in ['ground', 'ground2']:
        #     for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
        #         Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS['ground'])

        # water_frames = import_folder(os.path.join(os.path.dirname(__file__),'..', 'graphics', 'water'))
        # for x, y, surf in tmx_data.get_layer_by_name('water').tiles():
        #     Water(
        #         (x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites
        #     )

        # for obj in tmx_data.get_layer_by_name('groundobj'):
        #     Decors(
        #         (obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites]
        #     )
        
        # for obj in tmx_data.get_layer_by_name('trees'):
        #     Tree(
        #         (obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites]
        #     )
        
        self.player = Player((640, 360), self.all_sprites, self.collision_sprites)

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

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2


        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
        



