from csv import reader
import os
import pygame

def import_csv(path):
    terrain = []
    with open(path) as map:
        layout = reader(map, delimiter=',')
        for row in layout:
            terrain.append(list(row))
    
    return terrain

def import_folder(path, scale_factor = 1):
    surfaces = []
    for _, __, img_files in os.walk(path):
        for image in img_files:
            full_path = os.path.join(path, image)
            img_surf = pygame.image.load(full_path).convert_alpha()
            img_surf = pygame.transform.scale_by(img_surf, scale_factor)
            surfaces.append(img_surf)

    return surfaces

