import os

path = os.path.join('src', '..','graphics', 'overlay')


for root, dirs, img_files in os.walk(path):
    print(f"Current directory: {root}")  # Print current directory being accessed
    print(f"Subdirectories: {dirs}")  # Print list of subdirectories
    print(f"Image files: {img_files}")  # Print list of files in the directory

        # Check if we actually reached inside the directory
    if not os.path.exists(path):
        print(f"Path does not exist: {path}")

    if not any(os.scandir(path)):
        print(f"Directory is empty: {path}")
