import pygame
from settings import *
from support import *
import os
from timer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites):
        super().__init__(group)

        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0
        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        
        self.z = LAYERS['main']

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # collision
        self.hitbox = self.rect.copy()
        self.collision_sprites = collision_sprites

        # toggles
        self.timers = {
            'run' : Timer(750, self.run),
            'weapon_use' : Timer(750),
            'item_use' : Timer(750, self.item_use),
            'item_switch' : Timer(500)
        }

        # items
        self.items = ['r_potion', 'b_potion']
        self.item_index = 0
        self.selected_item = self.items[self.item_index]

    def run(self):
        if self.timers['run'].active:
            self.speed = 400
        else:
            self.speed = 200
        
    def item_use(self):
        pass

    def import_assets(self):
        self.animations = {
            'up_idle' : [], 'down_idle' : [], 'left_idle' : [], 'right_idle' : [],
            'up_walk' : [], 'down_walk' : [], 'left_walk' : [], 'right_walk' : [],
            'up_attack' : [], 'down_attack' : [], 'left_attack' : [], 'right_attack' : []
        }
        for animation in self.animations.keys():
            full_path = os.path.join(os.path.dirname(__file__), '..', 'graphics', 'character', animation)
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 6 * dt
        if self.frame_index > len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]
        self.image = pygame.transform.scale2x(self.image)

    def input(self):
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()

        if not self.timers['item_use'].active:

            # directions
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.status =  'up_walk'
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down_walk'
            else:
                self.direction.y = 0

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left_walk'
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right_walk'
            else:
                self.direction.x = 0
            
            # toggle
            if keys[pygame.K_SPACE] and not self.timers['run'].active:
                # timer for jump
                self.timers['run'].activate()
                self.frame_index = 0

            # item switch
            if mouse[0] and not self.timers['weapon_use'].active:
                self.timers['weapon_use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            if mouse[2] and not self.timers['item_use'].active:
                self.timers['item_use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0
            
    def get_status(self):
        # idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # attack
        if self.timers['weapon_use'].active:
            self.status = self.status.split('_')[0] + '_attack'
        
    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        # horitzontal collision
                        if self.direction.x > 0: # moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0: # moving left
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx

                    if direction == 'vertical':
                        # vertical collision
                        if self.direction.y > 0: # moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0: # moving up
                            self.hitbox.top = sprite.hitbox.bottom
                        
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def move(self, dt):
       
       # normalizing a vector
       if self.direction.magnitude() > 0:
           self.direction = self.direction.normalize()

        # horizontal movement
       self.pos.x += self.direction.x * self.speed * dt
       self.hitbox.centerx = round(self.pos.x)
       self.rect.centerx = self.hitbox.centerx
       self.collision('horizontal')

       # vertical movement
       self.pos.y += self.direction.y * self.speed * dt
       self.hitbox.centery = round(self.pos.y)
       self.rect.centery = self.hitbox.centery
       self.collision('vertical')

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.move(dt)
        self.animate(dt)

