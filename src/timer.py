import pygame

class Timer:
    def __init__(self, duration, func = None):
        self.duration = duration
        self.func = func
        self.start_timer = 0
        self.active = False

    def activate(self):
        self.active = True
        self.start_timer = pygame.time.get_ticks()

    def deactivate(self):
        self.active  = False
        self.start_timer = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_timer >= self.duration:
            self.deactivate()
        if self.func:
            self.func()