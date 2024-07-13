import os

def mass_rename(path):
    files = os.listdir(path)
    i = 0
    for filename in files:
        name, ext = os.path.splitext(filename)

        new_name = f"{i}" + ext
        os.rename(os.path.join(path, filename), os.path.join(path, new_name))
        i += 1

folder = ['walk', 'idle', 'attack']
sfolder = ['up', 'down', 'left', 'right']
for item in sfolder:
    file_path = os.path.join('graphics', 'character', 'enemies', 'slime', item)
    mass_rename(file_path)
        