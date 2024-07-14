import pygame
from math import exp
from settings import *
import os
from entity import Entity
from misc import import_folder

class Player(Entity):
    def __init__(self, pos, groups, obstacles, create_attack, kill_attack, use_item, kill_item):
        super().__init__(groups)
        self.image = pygame.image.load(os.path.join('graphics', 'character', 'player','down_idle', '0.png')).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 3)
        self.rect = self.image.get_rect(topleft = pos)

        # animation
        self.import_player_assets()
        self.status = 'down_idle'
        
        # attack
        self.attacking = False
        self.attack_cd = 700
        self.attack_time = None

        self.create_attack = create_attack
        self.kill_attack = kill_attack

        # item
        self.item_index = 0
        self.items = list(item_data.keys())[self.item_index]

        self.using_item = False
        self.item_cd = list(item_data.values())[self.item_index]['cooldown']
        self.use_time = None

        self.use_item = use_item
        self.kill_item = kill_item

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
        }
        self.max_stats = {
            'health' : 9999,
            'stamina' : 5000,
            'attack' : 150,
        }
        self.exp_curve = []

        self.lvl = 1
        self.health = self.stats['health']
        self.stamina = self.stats['stamina']
        self.exp = 0
        self.speed = 6

        # regeneration
        self.regen = True
        self.regen_rate = 0.5
        self.regen_time = None
        self.regen_cd = 100
        self.stamina_cost = 20

        # i-frames
        self.vulnerable = True
        self.hit_time = None
        self.invincible_duration = 600

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
            if keys[pygame.K_x] and not self.attacking and self.stamina >= self.stamina_cost:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            if keys[pygame.K_c] and not self.using_item:
                self.using_item = True
                self.use_time = pygame.time.get_ticks()

                item_type = list(item_data.keys())[self.item_index]
                heal = list(item_data.values())[self.item_index]['heal']

                self.use_item(item_type, heal)

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
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cd:
                self.attacking = False
                self.kill_attack()
        if not self.can_switch:
            if current_time - self.switch_timer >= self.switch_cd:
                self.can_switch = True
        
        if self.using_item:
            if current_time - self.use_time >= self.item_cd:
                self.using_item = False
                self.kill_item()

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincible_duration:
                self.vulnerable = True

    def stamina_regen(self):
        if self.attacking:
            self.regen = False
        else:
            current_time = pygame.time.get_ticks()
            if current_time - self.regen_cd >= 0:
                self.stamina += self.regen_rate
                if self.stamina >= self.stats['stamina']:
                    self.stamina = self.stats['stamina']

    def get_weapon_damage(self):
        return self.stats['attack']

    def lvl_up(self):
        # max attributes
        self.stats['health'] += 150
        self.stats['stamina'] += 50
        self.stats['exp'] += 70
        self.stats['attack'] += 10

        self.health = self.stats['health']
        self.stamina = self.stats['stamina']
        self.attack = self.stats['attack']
        self.lvl += 1


    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move()
        self.stamina_regen()