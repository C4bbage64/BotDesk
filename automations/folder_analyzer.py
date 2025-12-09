import os

def analyze_folder(folder_path):
    """Analyze the contents of a folder and returns a summary"""
    if not os.path.exists(folder_path):
        return "Error: The folder does not exist."

    file_count = 0
    folder_count = 0
    total_size = 0

    try:
        for root, dirs, files in os.walk(folder_path):
            folder_count += len(dirs)
            file_count += len(files)
            total_size += sum(os.path.getsize(os.path.join(root, f)) for f in files)

        result = (
            f"Folder Analysis:\n"
            f"Total Files: {file_count}\n"
            f"Total Folder: {folder_count}\n"
            f"Total Size: {total_size / (1024 * 1024):.2f} MB"
        )
        return result

    except Exception as e:
        return f"Error analyzing folder: {str(e)}"
