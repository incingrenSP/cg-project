import pygame, sys
from settings import *
from level import Level
from debug import debug

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Honkies")
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame .quit()
                    sys.exit()
                if event.type == pygame.MOUSEWHEEL:
                    self.level.player.timers['item_switch'].activate()
                    self.level.player.item_index += 1
                    self.level.player.item_index = self.level.player.item_index if self.level.player.item_index < len(self.level.player.items) else 0
                    self.level.player.selected_item = self.level.player.items[self.level.player.item_index]

            dt = self.clock.tick() / 1000
            self.level.run(dt)
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
