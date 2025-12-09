import os
import shutil
import zipfile

def compress_files(source_paths, output_path):
    """
    Compresses selected files and folders into a zip archive.
    
    Args:
        source_paths (list): List of absolute paths to files/folders to compress.
        output_path (str): Destination path for the .zip file.
        
    Returns:
        str: Success message or error message.
    """
    if not source_paths:
        return "No files selected for compression."
        
    try:
        # Ensure output path ends with .zip
        if not output_path.lower().endswith('.zip'):
            output_path += '.zip'
            
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for path in source_paths:
                if os.path.isfile(path):
                    # Add file, using its basename as arcname
                    zipf.write(path, os.path.basename(path))
                elif os.path.isdir(path):
                    # Add folder and its contents
                    base_folder = os.path.basename(path)
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            # Calculate relative path for arcname
                            rel_path = os.path.relpath(file_path, os.path.dirname(path))
                            zipf.write(file_path, rel_path)
                            
        return f"Successfully created archive: {output_path}"
    except Exception as e:
        return f"Error creating archive: {str(e)}"

def extract_archive(archive_path, output_dir):
    """
    Extracts an archive to the specified directory.
    
    Args:
        archive_path (str): Path to the archive file.
        output_dir (str): Destination directory.
        
    Returns:
        str: Success message or error message.
    """
    if not os.path.exists(archive_path):
        return "Archive file not found."
        
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        shutil.unpack_archive(archive_path, output_dir)
        return f"Successfully extracted to: {output_dir}"
    except Exception as e:
        return f"Error extracting archive: {str(e)}"
