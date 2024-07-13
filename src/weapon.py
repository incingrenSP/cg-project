import pygame, os

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        direction = player.status.split('_')[0]
        
        # graphics
        self.image = pygame.Surface((40, 40))

        # placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright)
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft)
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop)
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom)
        else:
            self.rect = self.image.get_rect(center = player.rect.center)