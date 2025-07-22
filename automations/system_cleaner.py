import os
import shutil
import tempfile

def clean_temp_files():
    """Cleans temporary files from the system."""
    temp_dir = tempfile.gettemdir()
    removed_files = []
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            try:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                removed_files.append(file_path)
            except Exception as e:
                pass  # ignore errors for system-locked files
    return f"Cleaned {len(removed_files)} temporary files."

def clean_cache(cache_dirs=None):
    """
    Cleans cache from the specified directories.

    :param cache_dirs: List of cache directories to clean. Default is browser cache locations.
    :return:
    """