import pygame

pygame.font.init()
font = pygame.font.Font(None, 30)

def debug(info, y = 10, x = 10):
    display_surface = pygame.display.get_surface()
    debug_surface = font.render(str(info), True, 'White')
    debug_rect = debug_surface.get_rect(topleft = (x, y))
    pygame.draw.rect(display_surface, 'Black', debug_rect)
    display_surface.blit(debug_surface, debug_rect)
    pygame.font.quit()