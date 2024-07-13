import os

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TILESIZE = 48

# items
item_data = {
    'potion' : [200, 50],
    'hi-potion' : [250, 150],
    'elixir' : [500, 9999]
}

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
STAMINA_BAR_WIDTH = 140
EXP_BAR_WIDTH = 180
ITEM_SIZE = 60
UI_FONT = os.path.join('fonts', 'mplus-1m-regular.woff')
UI_FONT_SIZE = 18

UI_BG_COLOR = 'black'
UI_BORDER_COLOR = 'yellow'
HEALTH_COLOR = 'red'
STAMINA_COLOR = 'green'
EXP_COLOR = 'blue'
