import pygame, os
from misc import import_folder

class Animator:
    def __init__(self):
        self.frames = {
            'fireball' : import_folder(os.path.join('graphics', 'particles', 'fireball')),
            'slash' : import_folder(os.path.join('graphics', 'particles', 'slash'), 0.2)
        }

    def generate_effect(self, pos, groups, animation_type):
        animations = self.frames[animation_type]
        ParticleEffect(pos, animations, groups)

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.1
        self.animations = frames
        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(center  = pos)

    def animate(self):
        # animate
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations):
            self.kill()
        else:
            self.image = self.animations[int(self.frame_index)]

    def update(self):
        self.animate()
