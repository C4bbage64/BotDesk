import os
import shutil

def organize_files(folder_path, extensions):
    if not os.path.exists(folder_path):
        return "Error: Folder path does not exist."

    try:
        for ext in extensions:
            ext_folder = os.path.join(folder_path, ext)
            os.makedirs(ext_folder, exist_ok=True)

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                file_ext = filename.split('.')[-1].lower()
                if file_ext in extensions:
                    shutil.move(file_path, os.path.join(folder_path, file_ext, filename))
        return "Files organized successfully!"
    except Exception as e:
        return f"Error: {str(e)}"
