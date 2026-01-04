import unittest
import os
import tempfile
from automations.system_cleaner import clean_temp_files, clean_cache
from automations.pdf_tools import merge_pdfs, split_pdfs, extract_text_from_pdf

class TestAutomations(unittest.TestCase):

    def test_clean_temp_files(self):
        # Create a dummy temp file
        temp_dir = tempfile.gettempdir()
        fd, path = tempfile.mkstemp(dir=temp_dir)
        os.close(fd)
        
        # Run cleaner
        result = clean_temp_files()
        
        # Verify file is gone (or at least the function ran without error)
        # Note: clean_temp_files might not delete *all* files due to locks, 
        # but it should try to delete our dummy file if it's not locked.
        # Since we just closed it, it should be deletable.
        self.assertFalse(os.path.exists(path), "Temp file should have been deleted")
        self.assertIn("Cleaned", result)

    def test_clean_cache_no_args(self):
        result = clean_cache()
        self.assertIn("No cache directories specified", result)

    def test_clean_cache_with_dir(self):
        # Create a dummy cache dir
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Create a file inside
            file_path = os.path.join(tmpdirname, "cache_file.txt")
            with open(file_path, "w") as f:
                f.write("data")
            
            result = clean_cache([tmpdirname])
            
            self.assertFalse(os.path.exists(file_path), "Cache file should be deleted")
            self.assertIn("Cleaned 1 files", result)

if __name__ == '__main__':
    unittest.main()
