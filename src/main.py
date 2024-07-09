import pygame, sys
from settings import *
from level import Level
import time

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Honkies")
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        last_time = time.time()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame .quit()
                    sys.exit()

            dt = time.time() - last_time
            last_time = time.time()
            self.level.run(dt)
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
