import os
import shutil

def move_file(file_path, dest_folder):
    """Move file to the destination folder"""
    if not os.path.exist(dest_folder):
        os.makedirs(dest_folder)
    shutil.move(file_path, os.path.join(dest_folder, os.path.basename(file_path)))