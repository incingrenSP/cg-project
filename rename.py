import os

def mass_rename(path):
    files = os.listdir(path)
    i = 0
    for filename in files:
        name, ext = os.path.splitext(filename)

        new_name = f"{i}" + ext
        os.rename(os.path.join(path, filename), os.path.join(path, new_name))
        i += 1
        
folder = ['walk', 'run']
sfolder = ['up', 'down', 'left', 'right']
for item in folder:
    for file in sfolder:
        path = file + '_' + item
        file_path = os.path.join('graphics', 'character', path)
        mass_rename(file_path)

# file_path = os.path.join('graphics', 'water')
# mass_rename(file_path)