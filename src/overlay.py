import pygame, os
from settings import *

class Overlay:
    def __init__(self, player):
        
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # imports
        overlay_path = os.path.join(os.path.dirname(__file__), '..', 'graphics', 'overlay')
        self.weapon_surface = {weapon:pygame.image.load(f'{overlay_path}/{weapon}.png') for weapon in player.weapons}
        self.item_surface = {item:pygame.image.load(f'{overlay_path}/{item}.png') for item in player.items}

    def display(self):
        # show weapons
        weapon_surface = self.weapon_surface[self.player.selected_weapon]
        weapon_rect = weapon_surface.get_rect(midbottom=OVERLAY_POSITIONS['weapons'])
        self.display_surface.blit(weapon_surface, weapon_rect)

        # show items
        item_surface = self.item_surface[self.player.selected_item]
        item_rect = item_surface.get_rect(midbottom = OVERLAY_POSITIONS['items'])
        self.display_surface.blit(item_surface, item_rect)

        


