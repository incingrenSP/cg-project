import pygame
from settings import *
import os
from misc import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles, create_attack, kill_attack):
        super().__init__(groups)
        self.image = pygame.image.load(os.path.join('graphics', 'character', 'player','down_idle', '0.png')).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 3)
        self.rect = self.image.get_rect(topleft = pos)

        # animation
        self.import_player_assets()
        self.status = 'down_idle'
        self.frame_index = 0
        self.animation_speed = 0.1

        # movement
        self.direction = pygame.math.Vector2()

        # attack/items
        self.attacking = False
        self.attack_cd = 800
        self.attack_time = None

        self.create_attack = create_attack
        self.kill_attack = kill_attack
        self.item_index = 0
        self.items = list(item_data.keys())[self.item_index]

        self.can_switch = True
        self.switch_timer = None
        self.switch_cd = 200

        # collision
        self.obstacle_sprites = obstacles
        self.hitbox = self.rect.inflate(0, 0)

        # player stats
        self.stats = {
            'health' : 100,
            'stamina' : 50,
            'exp' : 500,
            'attack' : 10,
            'speed' : 15,
        }
        self.health = self.stats['health']
        self.stamina = self.stats['stamina']
        self.exp = 0
        self.speed = 3

    def import_player_assets(self):
        import_folder_path = os.path.join('graphics', 'character', 'player')
        self.animation = {
            'up_idle' : [], 'down_idle' : [], 'left_idle' : [], 'right_idle' : [],
            'up_walk' : [], 'down_walk' : [], 'left_walk' : [], 'right_walk' : [],
            'up_attack' : [], 'down_attack' : [], 'left_attack' : [], 'right_attack' : []
        }
        for animation in self.animation.keys():
            full_path = os.path.join(import_folder_path, animation)
            self.animation[animation] = import_folder(full_path, 3)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.attacking:
            # MOVEMENT INPUT
            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left_walk'
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right_walk'
            else:
                self.direction.x = 0
            
            if keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down_walk'
            elif keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up_walk'
            else:
                self.direction.y = 0

            # ATTACK INPUT
            if keys[pygame.K_x] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
            if keys[pygame.K_v] and self.can_switch:
                self.can_switch = False
                self.switch_timer = pygame.time.get_ticks()

                self.item_index += 1
                if self.item_index >= len(item_data.keys()):
                    self.item_index = 0
                self.items = list(item_data.keys())[self.item_index]

    def get_status(self):
        # idling
        if self.direction.x == 0 and self.direction.y == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # attack
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            self.status = self.status.split('_')[0] + '_attack'

    def animate(self):
        animation = self.animation[self.status]

        # animate
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        # right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        # left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        # down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        # up
                        self.hitbox.top = sprite.hitbox.bottom

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * self.speed
        self.collision('horizontal')

        self.hitbox.y += self.direction.y * self.speed
        self.collision('vertical')

        self.rect.center = self.hitbox.center

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cd:
                self.attacking = False
                self.kill_attack()
        if not self.can_switch:
            if current_time - self.switch_timer >= self.switch_cd:
                self.can_switch = True

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move()