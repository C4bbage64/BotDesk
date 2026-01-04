import os
import shutil
import unittest
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from automations.batch_renamer import get_rename_preview, execute_renames
from automations.zip_manager import compress_files, extract_archive

class TestNewFeatures(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_env"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)
        
        # Create dummy files
        self.files = ["file1.txt", "file2.txt", "image.png"]
        for f in self.files:
            with open(os.path.join(self.test_dir, f), 'w') as fh:
                fh.write("content")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_batch_renamer(self):
        print("\nTesting Batch Renamer...")
        # Test Preview
        preview = get_rename_preview(self.test_dir, add_prefix="test_")
        self.assertEqual(len(preview), 3)
        self.assertEqual(preview[0][1], "test_file1.txt")
        
        # Test Execution
        rename_map = {old: new for old, new in preview}
        msg, errors = execute_renames(self.test_dir, rename_map)
        self.assertTrue("Successfully renamed 3 files" in msg)
        self.assertEqual(len(errors), 0)
        
        # Verify files exist
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "test_file1.txt")))
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "file1.txt")))
        print("Batch Renamer Passed!")

    def test_zip_manager(self):
        print("\nTesting Zip Manager...")
        # Test Compression
        files_to_zip = [os.path.join(self.test_dir, f) for f in os.listdir(self.test_dir)]
        zip_path = os.path.join(self.test_dir, "archive.zip")
        
        msg = compress_files(files_to_zip, zip_path)
        self.assertTrue("Successfully created archive" in msg)
        self.assertTrue(os.path.exists(zip_path))
        
        # Test Extraction
        extract_dir = os.path.join(self.test_dir, "extracted")
        msg = extract_archive(zip_path, extract_dir)
        self.assertTrue("Successfully extracted" in msg)
        

        # Verify extracted content
        self.assertTrue(os.path.exists(os.path.join(extract_dir, "file1.txt")))
        print("Zip Manager Passed!")

    def test_undo_rename(self):
        print("\nTesting Undo Functionality...")
        # 1. Rename
        preview = get_rename_preview(self.test_dir, add_prefix="undo_test_")
        rename_map = {old: new for old, new in preview}
        execute_renames(self.test_dir, rename_map)
        
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "undo_test_file1.txt")))
        
        # 2. Undo (Reverse Rename)
        reverse_map = {new: old for old, new in rename_map.items()}
        msg, errors = execute_renames(self.test_dir, reverse_map)
        
        self.assertEqual(len(errors), 0)
        self.assertTrue("Successfully renamed" in msg)
        
        # 3. Verify Reversion
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "file1.txt")))
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "undo_test_file1.txt")))
        print("Undo Functionality Passed!")

if __name__ == '__main__':
    unittest.main()
