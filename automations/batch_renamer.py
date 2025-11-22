import os

def get_rename_preview(folder_path, replace_text="", with_text="", add_prefix="", add_suffix=""):
    """
    Generates a preview of file renames based on the provided criteria.
    
    Args:
        folder_path (str): Path to the folder containing files.
        replace_text (str): Text to replace in the filename.
        with_text (str): Text to replace with.
        add_prefix (str): Text to add to the beginning of the filename.
        add_suffix (str): Text to add to the end of the filename (before extension).
        
    Returns:
        list: A list of tuples (original_name, new_name) for files that will be changed.
    """
    preview = []
    if not os.path.exists(folder_path):
        return []

    try:
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    except Exception:
        return []
    
    for filename in files:
        new_name = filename
        name, ext = os.path.splitext(filename)
        
        # Replace text
        if replace_text:
            new_name = new_name.replace(replace_text, with_text)
            # Re-split in case replacement affected extension (though usually we operate on full name or just base?)
            # Standard behavior: replace in the whole name including extension? 
            # Or just base? Let's do whole name for flexibility, but usually people want base.
            # Let's stick to simple string replacement on the whole name for now, 
            # but prefix/suffix usually apply to base.
            
            # Actually, let's refine: Replace usually applies to the whole string.
            # Prefix/Suffix apply to the base name.
            
            # Let's re-calculate name/ext after replacement if we want to be safe, 
            # but if we replace in 'new_name', we are modifying the whole thing.
            pass

        # Apply prefix/suffix to the current state of the name (excluding extension for suffix)
        # To do this correctly, we need to split the potentially modified new_name
        current_base, current_ext = os.path.splitext(new_name)
        
        if add_prefix:
            current_base = f"{add_prefix}{current_base}"
            
        if add_suffix:
            current_base = f"{current_base}{add_suffix}"
            
        final_name = f"{current_base}{current_ext}"
        
        if final_name != filename:
            preview.append((filename, final_name))
            
    return preview

def execute_renames(folder_path, rename_map):
    """
    Executes the renaming of files based on a map of {old_name: new_name}.
    
    Args:
        folder_path (str): Path to the folder.
        rename_map (dict): Dictionary mapping original filenames to new filenames.
        
    Returns:
        tuple: (success_message, error_list)
    """
    renamed_count = 0
    errors = []
    
    if not os.path.exists(folder_path):
        return "Folder not found.", ["Folder does not exist."]

    for old_name, new_name in rename_map.items():
        if old_name == new_name:
            continue
            
        try:
            old_path = os.path.join(folder_path, old_name)
            new_path = os.path.join(folder_path, new_name)
            
            if os.path.exists(new_path):
                errors.append(f"Skipped {old_name}: Destination {new_name} already exists.")
                continue
                
            os.rename(old_path, new_path)
            renamed_count += 1
        except Exception as e:
            errors.append(f"Error renaming {old_name}: {str(e)}")
            
    return f"Successfully renamed {renamed_count} files.", errors
