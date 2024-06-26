import pygame, sys

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
WIDTH = 64
HEIGHT = 128
scale = 3

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Test Program')
clock = pygame.time.Clock()

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, color):
        img = pygame.Surface((width, height)).convert_alpha()
        img.blit(self.sheet, (0, 0), (width * frame, 0, width, height))
        img = pygame.transform.scale(img, (width * scale, height * scale))
        img.set_colorkey(color)

        return img


sprite_sheet_img = pygame.image.load('graphics/character/idle/idle.png').convert_alpha()
sprite_sheet = SpriteSheet(sprite_sheet_img)

frames = [
    sprite_sheet.get_image(0, WIDTH, HEIGHT, scale, 'black'),
    sprite_sheet.get_image(1, WIDTH, HEIGHT, scale, 'black'),
    sprite_sheet.get_image(2, WIDTH, HEIGHT, scale, 'black'),
    sprite_sheet.get_image(3, WIDTH, HEIGHT, scale, 'black')
]

if __name__ == '__main__':
    running = True
    while running:
        screen.fill('gray')
        i = 0
        for frame in frames:
            screen.blit(frame, (WIDTH * i * scale, 0))
            i += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)
        pygame.display.update()
    
    pygame.quit()
    sys.exit()

