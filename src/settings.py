import os

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TILESIZE = 48

# items
item_data = {
    'potion' : {'cooldown' : 200, 'heal' : 50, 'graphics' : os.path.join('graphics', 'icons', 'potion.png')},
    'hi-potion' : {'cooldown' : 200, 'heal' : 150, 'graphics' : os.path.join('graphics', 'icons', 'hi_potion.png')},
    'elixir' : {'cooldown' : 200, 'heal' : 1000, 'graphics' : os.path.join('graphics', 'icons', 'elixir.png')}
}

# enemies
enemy_data = {
    'dragon' : {'health' : 2000, 'damage' : 150, 'exp' : 5000, 'speed' : 3, 'attack_range' : 400, 'detection_range' : 500},
    'slime' : {'health' : 20, 'damage' : 3, 'exp' : 30, 'speed' : 3, 'attack_range' : 100, 'detection_range' : 300}
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
