import os
import pygame

def import_folder(path):
    surface_list = []
    for _, __, img_files in os.walk(path): # graphics/character/up_idle
        for image in img_files:
            full_path = os.path.join(path, image)
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list