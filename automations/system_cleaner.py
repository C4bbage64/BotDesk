import os
import shutil
import tempfile

def clean_temp_files():
    """Cleans temporary files from the system."""
    temp_dir = tempfile.gettempdir()
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

    :param cache_dirs: List of cache directories to clean. Default is None.
    :return: Summary string.
    """
    if cache_dirs is None:
        # Placeholder for common browser cache paths or other temp locations
        # For safety, we won't guess user paths without explicit configuration
        return "No cache directories specified. Skipping cache cleanup."
    
    cleaned_count = 0
    for directory in cache_dirs:
        if os.path.exists(directory):
            for root, dirs, files in os.walk(directory):
                for file in files:
                    try:
                        os.remove(os.path.join(root, file))
                        cleaned_count += 1
                    except Exception:
                        pass
    return f"Cleaned {cleaned_count} files from cache directories."