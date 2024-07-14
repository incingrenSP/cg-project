import os

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TILESIZE = 48

# items
item_data = {
    'potion' : {'cooldown' : 200, 'heal' : 50, 'graphics' : os.path.join('graphics', 'icons', 'potion.png')},
    'hi-potion' : {'cooldown' : 200, 'heal' : 500, 'graphics' : os.path.join('graphics', 'icons', 'hi_potion.png')},
    'elixir' : {'cooldown' : 200, 'heal' : 1000, 'graphics' : os.path.join('graphics', 'icons', 'elixir.png')}
}

# enemies
enemy_data = {
    'dragon' : {'health' : 2000, 'damage' : 100, 'exp' : 5000, 'speed' : 4, 'knock_back' : 1000,'attack_range' : 300, 'detection_range' : 700, 'attack_type' : 'fireball'},
    'slime' : {'health' : 20, 'damage' : 8, 'exp' : 200, 'speed' : 3, 'knock_back' : 350,'attack_range' : 50, 'detection_range' : 300, 'attack_type' : 'slash'}
}

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
STAMINA_BAR_WIDTH = 140
EXP_BAR_WIDTH = 180
ITEM_SIZE = 60
UI_FONT = os.path.join('fonts', 'mplus-1m-regular.woff')
UI_FONT_SIZE = 18

UI_BG_COLOR = '#404040'
UI_BORDER_COLOR = '#ff9d47'
HEALTH_COLOR = '#b50030'
STAMINA_COLOR = '#24875e'
EXP_COLOR = '#d9ff42'
