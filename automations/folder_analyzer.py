import os

def analyze_folder(folder_path, progress_callback=None):
    """
    Analyze the contents of a folder and returns a detailed summary dictionary.
    
    Args:
        folder_path (str): Path to analyze
        progress_callback (callable): Optional function to call with progress updates (e.g. file count)
        
    Returns:
        dict: Analysis results
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
            
            # Update progress periodically
            if progress_callback and file_count % 100 == 0:
                progress_callback(file_count)

            # Calculate size of current folder (just files in it)
            current_folder_size = 0
            
            for f in files:
                file_count += 1
                fp = os.path.join(root, f)
                try:
                    size = os.path.getsize(fp)
                    total_size += size
                    current_folder_size += size
                    all_files.append((fp, size))
                except OSError:
                    pass # Skip files we can't access
            
            folder_sizes[root] = current_folder_size

        # Propagate sizes for cumulative folder size
        # We need to process from deepest to shallowest
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
