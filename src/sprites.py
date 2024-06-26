import pygame
from settings import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = LAYERS['main']):
        super().__init__(groups)
        self.image = pygame.transform.scale(surf, (10000, 10000))
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z


