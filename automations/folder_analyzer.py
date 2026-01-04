import os

def analyze_folder(folder_path):
    """
    Analyze the contents of a folder and returns a detailed summary dictionary.
    Returns:
        dict: {
            'total_files': int,
            'total_folders': int,
            'total_size': int (bytes),
            'top_files': list of (path, size),
            'top_folders': list of (path, size)
        }
    """
    if not os.path.exists(folder_path):
        raise ValueError("The folder does not exist.")

    file_count = 0
    folder_count = 0
    total_size = 0
    
    all_files = [] # Listen of (path, size)
    folder_sizes = {} # path -> size

    try:
        # First pass: Walk to get all files and calculate sizes
        for root, dirs, files in os.walk(folder_path):
            folder_count += len(dirs)
            file_count += len(files)
            
            # Calculate size of current folder (just files in it)
            current_folder_size = 0
            
            for f in files:
                fp = os.path.join(root, f)
                try:
                    size = os.path.getsize(fp)
                    total_size += size
                    current_folder_size += size
                    all_files.append((fp, size))
                except OSError:
                    pass # Skip files we can't access
            
            # Add to directory sizes (this is direct size, we might want cumulative)
            # For "Largest Folders", usually users mean cumulative size (including subfolders).
            # We'll need a way to propagate sizes up.
            folder_sizes[root] = current_folder_size

        # Propagate sizes for cumulative folder size
        # We need to process from deepest to shallowest
        sorted_folders = sorted(folder_sizes.keys(), key=lambda x: x.count(os.sep), reverse=True)
        cumulative_sizes = {}
        
        for folder in sorted_folders:
            size = folder_sizes.get(folder, 0)
            # Add this folder's size to its parent
            parent = os.path.dirname(folder)
            
            # Initialize if not set (for the current folder)
            if folder not in cumulative_sizes:
                cumulative_sizes[folder] = size
            else:
                cumulative_sizes[folder] += size
            
            # Add to parent logic would be tricky because os.walk covers everything.
            # Wait, os.walk hits every folder. 
            # If I sum all files in a tree, I get the total.
            # To get "Folder Size", I should sum all files where 'folder' is a prefix of file path.
            # But that's O(N*M).
            
            # Better approach:
            # os.walk is top-down by default. 'topdown=False' makes it bottom-up.
        
        # Let's redo the walk with bottom-up for easier cumulative calculation
        folder_cum_sizes = {}
        
        for root, dirs, files in os.walk(folder_path, topdown=False):
            # Files size in this dir
            local_size = sum(os.path.getsize(os.path.join(root, f)) for f in files if os.path.exists(os.path.join(root, f)))
            
            # Subdir sizes (already calculated because bottom-up)
            subdir_size = sum(folder_cum_sizes.get(os.path.join(root, d), 0) for d in dirs)
            
            total_folder_size = local_size + subdir_size
            folder_cum_sizes[root] = total_folder_size

        # Sort for top 50
        top_files = sorted(all_files, key=lambda x: x[1], reverse=True)[:50]
        
        # For folders, we might want to exclude the root itself from the list if it's just "the whole drive"
        # But showing it is fine.
        top_folders = sorted(folder_cum_sizes.items(), key=lambda x: x[1], reverse=True)[:50]

        return {
            'total_files': file_count,
            'total_folders': folder_count,
            'total_size': total_size,
            'top_files': top_files,
            'top_folders': top_folders
        }

    except Exception as e:
        raise Exception(f"Error analyzing folder: {str(e)}")
