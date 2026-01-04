import os
import shutil
from core.commands import Command
from automations.image_optimizer import optimize_image

class BatchOptimizeCommand(Command):
    """
    Command to optimize a batch of images.
    Supports Undo by restoring original files from backup or deleting new files.
    """
    def __init__(self, file_paths, output_dir, quality, max_width, format):
        self.file_paths = file_paths
        self.output_dir = output_dir
        self.quality = quality
        self.max_width = max_width
        self.format = format
        
        # Tracks created files for undo: {original_path: created_path}
        self.created_files = {} 
        # Tracks backups for overwrite/in-place optimization (if we supported it, 
        # allowing complexity for now, we are creating NEW files mostly)
        
    def execute(self):
        results = []
        errors = []
        
        for file_path in self.file_paths:
            try:
                new_path = optimize_image(
                    file_path, 
                    self.output_dir, 
                    self.quality, 
                    self.max_width, 
                    self.format
                )
                self.created_files[file_path] = new_path
                results.append(new_path)
            except Exception as e:
                errors.append(f"{os.path.basename(file_path)}: {e}")
                
        return len(results), errors

    def undo(self):
        """
        Undo operation: Deletes the optimized images that were created.
        """
        for original, new_path in self.created_files.items():
            if os.path.exists(new_path):
                os.remove(new_path)
        self.created_files.clear()
