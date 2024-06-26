import pygame, sys
from pytmx.util_pygame import load_pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
tmx_data = load_pygame('data/world.tmx')

# get layers
print(tmx_data.layers)  # get all layers
for layer in tmx_data.visible_layers:   # get visible layers
    print(layer)

print(tmx_data.layernames)  # get all layer names as dict

print(tmx_data.get_layer_by_name('groundobj')) # get one layer by name

for obj in tmx_data.objectgroups:   # get object layers
    print(obj)

# get tiles
layer = tmx_data.get_layer_by_name('ground')
# for x,y, surf in layer.tiles():
#     print(x)
#     print(y)
#     print(surf)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')
    clock.tick(60)
    pygame.display.update()
