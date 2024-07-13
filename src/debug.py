import pygame
pygame.init()
font = pygame.font.Font('fonts/mplus-1m-regular.woff', 30)

def debug(info, y = 10, x = 1260):
    display_surf = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, 'white')
    debug_rect = debug_surf.get_rect(topleft = (x, y))
    pygame.draw.rect(display_surf, 'black', debug_rect)
    display_surf.blit(debug_surf, debug_rect)