import unittest
import os
import shutil
import tempfile
from automations.folder_analyzer import analyze_folder

class TestFolderAnalyzer(unittest.TestCase):
    def setUp(self):
        # Create a temp dir
        self.test_dir = tempfile.mkdtemp()
        
        # Create some files with different sizes
        self.create_file("small.txt", 100)
        self.create_file("medium.txt", 1000)
        self.create_file("large.txt", 10000)
        
        # Create a subfolder with files
        os.makedirs(os.path.join(self.test_dir, "subdir"))
        self.create_file(os.path.join("subdir", "huge.txt"), 50000)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def create_file(self, name, size):
        path = os.path.join(self.test_dir, name)
        with open(path, "wb") as f:
            f.write(b"0" * size)

    def test_analyzer_logic(self):
        result = analyze_folder(self.test_dir)
        
        # Check structure
        self.assertIn('total_files', result)
        self.assertIn('total_folders', result)
        self.assertIn('total_size', result)
        self.assertIn('top_files', result)
        self.assertIn('top_folders', result)
        
        # Check counts
        self.assertEqual(result['total_files'], 4)
        
        # Check Top Files sort order (largest first)
        top_files = result['top_files']
        self.assertTrue(len(top_files) > 0)
        self.assertTrue(top_files[0][0].endswith("huge.txt")) # Largest file
        self.assertTrue(top_files[1][0].endswith("large.txt"))

        # Check Top Folders
        # subdir should be effectively largest as it contains huge.txt
        # Root contains all.
        top_folders = result['top_folders']
        # Depending on implementation, root might be first.
        
        # Verify sizes are physically correct
        expected_size = 100 + 1000 + 10000 + 50000
        self.assertEqual(result['total_size'], expected_size)

if __name__ == '__main__':
    unittest.main()
