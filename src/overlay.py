import pygame, os
from settings import *

class Overlay:
    def __init__(self, player):
        
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # imports
        overlay_path = os.path.join(os.path.dirname(__file__), '..', 'graphics', 'overlay')
        self.item_surface = {item:pygame.image.load(f'{overlay_path}/{item}.png') for item in player.items}

    def display(self):
        # show items
        item_surface = self.item_surface[self.player.selected_item]
        item_rect = item_surface.get_rect(midbottom = OVERLAY_POSITIONS['items'])
        self.display_surface.blit(item_surface, item_rect)

        


