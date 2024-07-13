import pygame
from settings import *

class UI:
    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.stamina_bar_rect = pygame.Rect(10, 34, STAMINA_BAR_WIDTH, BAR_HEIGHT)
        self.exp_bar_rect = pygame.Rect(10, 58, EXP_BAR_WIDTH, BAR_HEIGHT)

        # icon setup
        self.item_graphics = []
        for items in item_data.values():
            path = items['graphics']
            item = pygame.image.load(path)
            item = pygame.transform.scale_by(item, 3)
            self.item_graphics.append(item)

    def show_bar(self, current_amount, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # convert stats
        ratio = current_amount / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # draw bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_lvl(self, lvl):
        text_surf = self.font.render(f'Lv: {str(int(lvl))}', False, 'white')
        x = SCREEN_WIDTH - 20
        y = SCREEN_HEIGHT - 20
        text_rect = text_surf.get_rect(bottomright = (x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(15, 15))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(15, 15), 3)

    def selection_box(self, left, top):
        bg_rect = pygame.Rect(left, top, ITEM_SIZE, ITEM_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        return bg_rect

    def item_overlay(self, item_index):
        bg_rect = self.selection_box(10, 650)
        item_surf = self.item_graphics[item_index]
        item_rect = item_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(item_surf, item_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

        text_surf = self.font.render(f'{str(list(item_data.keys())[item_index])}', False, 'white')
        x = 80
        y = SCREEN_HEIGHT - 20
        text_rect = text_surf.get_rect(bottomleft = (x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(15, 15))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(15, 15), 3)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.stamina, player.stats['stamina'], self.stamina_bar_rect, STAMINA_COLOR)
        self.show_bar(player.exp, player.stats['exp'], self.exp_bar_rect, EXP_COLOR)

        self.show_lvl(player.lvl)
        self.item_overlay(player.item_index)
        