import os
from PIL import Image

def optimize_image(file_path, output_dir=None, quality=85, max_width=None, convert_to=None):
    """
    Optimizes an image: resizes, compresses, and optionally converts format.
    Returns the path to the new image.
    """
    try:
        img = Image.open(file_path)
        filename = os.path.basename(file_path)
        name, ext = os.path.splitext(filename)
        
        # Determine output format and extension
        if convert_to:
            ext = f".{convert_to.lower()}"
            format_name = convert_to.upper()
        else:
            format_name = img.format 
            if format_name == 'JPEG': 
                ext = '.jpg'

        # Determine output path
        if output_dir:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            save_path = os.path.join(output_dir, name + ext)
        else:
            # If overwriting or same folder, careful not to clobber unless intended?
            # For this feature, let's append suffix if same folder
            save_path = os.path.join(os.path.dirname(file_path), name + "_optimized" + ext)

        # Resize if max_width is set
        if max_width and img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

        # Convert to RGB if saving as JPEG (handle transparency)
        if format_name in ('JPEG', 'JPG') and img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        # Save
        img.save(save_path, quality=quality, optimize=True)
        return save_path

    except Exception as e:
        raise Exception(f"Failed to process {file_path}: {e}")
