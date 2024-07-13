import pygame, os
from settings import *
from misc import *
from entity import Entity

class Enemy(Entity):
    def __init__(self, enemy_name, pos, groups, obstacle_sprites, damage_player):
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # graphics
        self.import_graphics(enemy_name)
        self.status = 'down'
        self.image = self.animations[self.status][int(self.frame_index)]

        # movement
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.copy()
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.enemy_name = enemy_name
        enemy_info = enemy_data[self.enemy_name]
        self.health = enemy_info['health']
        self.damage = enemy_info['damage']
        self.exp = enemy_info['exp']
        self.speed = enemy_info['speed']
        self.knock_back = enemy_info['knock_back']
        self.attack_range = enemy_info['attack_range']
        self.detection_range = enemy_info['detection_range']

        # interactions
        self.can_attack = True
        self.attack_time = None
        self.attack_cd = 800

        self.damage_player = damage_player

        # i-frames
        self.vulnerable = True
        self.hit_time = None
        self.invincible_duration = 600

    def import_graphics(self, name):
        self.animations = {
            'down' : [], 'left' : [], 'right' : [], 'up' : []
        }
        main_path = os.path.join('graphics', 'character', 'enemies', f'{name}')
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(os.path.join(main_path, animation))

    def get_player_distance(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)

        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def actions(self, player):
        distance = self.get_player_distance(player)[0]
        if distance <= self.attack_range and self.can_attack:
            self.damage_player(self.damage)
            self.can_attack = False
            self.attack_time = pygame.time.get_ticks()
        elif distance <= self.detection_range:
            self.direction = self.get_player_distance(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def check_status(self):
        if self.direction.x == 1:
            self.status = 'right'
        elif self.direction.x == -1:
            self.status = 'left'
        if self.direction.y == 1:
            self.status = 'down'
        elif self.direction.y == -1:
            self.status = 'up'
        
    def animate(self):
        animation = self.animations[self.status]

        # animate
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.image = pygame.transform.scale_by(self.image, 3)
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cd:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincible_duration:
                self.vulnerable = True

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.get_player_distance(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_weapon_damage()

            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.kill()

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.knock_back

    def update(self):
        self.hit_reaction()
        self.cooldowns()
        self.check_status()
        self.animate()
        self.move()
        self.check_death()

    def enemy_update(self, player):
        self.actions(player)
        
class Dragon(Enemy):
    def __init__(self, pos, groups, obstacle_sprites, damage_player):
        super().__init__('dragon', pos, groups, obstacle_sprites, damage_player)

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * self.speed
        self.hitbox.y += self.direction.y * self.speed

        self.rect.center = self.hitbox.center
        
    def update(self):
        self.hit_reaction()
        self.cooldowns()
        self.check_status()
        self.animate()
        self.move()
        self.check_death()

    def enemy_update(self, player):
        self.actions(player)

