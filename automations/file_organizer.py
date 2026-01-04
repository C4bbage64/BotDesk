import os
import shutil

def organize_files(folder_path, extensions):
    """
    Organizes files in the given folder into subfolders based on their extensions.

    :param folder_path: Path to the folder to organize
    :param extensions: List of file extensions to organize
    :return: Success or error message
    """
    if not os.path.isdir(folder_path):
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
                    dest_folder = os.path.join(folder_path, file_ext)
                    shutil.move(file_path, os.path.join(dest_folder, filename))
        return "Files organized successfully."
    except Exception as e:
        return f"Error: {str(e)}"

