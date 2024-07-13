import pygame, os, random
from settings import *
from misc import *
from sprites import Tile
from player import Player
from enemy import Enemy, Dragon
from weapon import Weapon
from ui import UI
from particle import Animator
from debug import debug

class Level:
    def __init__(self):
        # render surface
        self.display_surf = pygame.display.get_surface()

        self.all_sprites = CameraGroup()    # sprites that are rendered
        self.collision_sprites = pygame.sprite.Group()  # sprites that interact via collisions
        self.attack_sprites = pygame.sprite.Group() # sprites that can attack
        self.attackable_sprites = pygame.sprite.Group() # sprites that can be attacked

        # attack sprites
        self.current_attack = None
        self.current_item = None

        # drawing the game
        self.create_map()

        # ui
        self.ui = UI()

        # particles
        self.animator = Animator()

    def create_map(self):
        layouts = {
            'boundary' : import_csv(os.path.join('data', 'map_blocktiles.csv')),
            'flowers' : import_csv(os.path.join('data', 'map_flowers.csv')),
            'objects' : import_csv(os.path.join('data', 'map_objects.csv'))
        }
        graphics = {
            'flowers' : import_folder(os.path.join('graphics', 'weed')),
            'objects' : import_folder(os.path.join('graphics', 'obstacles'))
        }
        
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):

                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        if style == 'boundary':
                            Tile((x, y), self.collision_sprites, 'invisible')

                        if style == 'flowers':
                            random_flower = random.choice(graphics['flowers'])
                            Tile((x, y), [self.all_sprites, self.collision_sprites, self.attackable_sprites], 'grass', random_flower)

                        if style == 'objects':
                            obj_surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.all_sprites, self.collision_sprites], 'object', obj_surf)
                        
        Dragon(
            (64 * TILESIZE, 19 * TILESIZE),
            [self.all_sprites, self.attackable_sprites],
            self.collision_sprites,
            self.damage_player,
            self.add_exp
        )

        Enemy(
            'slime',
            (52 * TILESIZE, 49 * TILESIZE),
            [self.all_sprites, self.attackable_sprites],
            self.collision_sprites,
            self.damage_player,
            self.add_exp
        )

        self.player = Player(
            (62 * TILESIZE, 48 * TILESIZE),
            self.all_sprites,
            self.collision_sprites,
            self.spawn_attack,
            self.despawn_attack,
            self.use_item,
            self.kill_item
            )

    def spawn_attack(self):
        self.current_attack = Weapon(self.player, [self.attack_sprites])

    def use_item(self, item_type, heal):
        if item_type in ['potion', 'hi_potion', 'elixir']:
            self.player.health += heal
            if self.player.health > self.player.stats['health']:
                self.player.health = self.player.stats['health']

    def despawn_attack(self):
        if self.current_attack:
            self.player.stamina -= 20
            self.current_attack.kill()
        self.current_attack = None

    def kill_item(self):
        if self.current_item:
            self.current_item.kill()
        self.current_item = None

    def player_attack(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                colliding_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if colliding_sprites:
                    for target_sprite in colliding_sprites:
                        if target_sprite.sprite_type == 'grass':
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hit_time = pygame.time.get_ticks()
            # spawn particles
            self.animator.generate_effect(self.player.rect.center, self.all_sprites, attack_type)

    def add_exp(self, amount):
        self.player.exp += amount
        while self.player.exp >= self.player.stats['exp']:
            self.player.exp -= self.player.stats['exp']
            self.player.lvl_up()

    def run(self):
        # update and draw
        self.display_surf.fill('black')
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update()
        self.all_sprites.enemy_update(self.player)
        self.player_attack()
        self.ui.display(self.player)

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        # setup
        self.display_surf = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

        self.floor_surf = pygame.image.load(os.path.join('graphics', 'world', 'world.png')).convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))

    def custom_draw(self, player):
        # getting offset
        self.offset.x = player.rect.centerx - SCREEN_WIDTH // 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT // 2

        # floor
        floor_offset = self.floor_rect.topleft - self.offset
        self.display_surf.blit(self.floor_surf, floor_offset)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surf.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)