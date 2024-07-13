import pygame
from settings import *
import os

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.copy()


class Water(Tile):
    def __init__(self, pos, frames, groups):    
        # animation setup
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = 0.1

        super().__init__(
            pos = pos,
            groups = groups,
            sprite_type = 'water',
            surface = self.frames[self.frame_index],
        )

    def animate(self):
        animation = self.frames

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()


    