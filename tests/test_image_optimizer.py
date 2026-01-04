import unittest
import os
import shutil
from PIL import Image
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from commands.image_commands import BatchOptimizeCommand
from core.commands import CommandInvoker

class TestImageOptimizer(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_images"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)
        
        # Create dummy image
        self.img_path = os.path.join(self.test_dir, "test.png")
        img = Image.new('RGB', (1000, 1000), color='red')
        img.save(self.img_path)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_optimization_command(self):
        print("\nTesting Image Optimizer Command...")
        invoker = CommandInvoker()
        
        # Execute Optimization (Resize to 100px)
        cmd = BatchOptimizeCommand(
            file_paths=[self.img_path],
            output_dir=None,
            quality=80,
            max_width=100,
            format='jpg'
        )
        
        count, errors = cmd.execute()
        self.assertEqual(count, 1)
        self.assertEqual(len(errors), 0)
        
        # Verify Output
        expected_output = os.path.join(self.test_dir, "test_optimized.jpg")
        self.assertTrue(os.path.exists(expected_output))
        
        with Image.open(expected_output) as img:
            self.assertEqual(img.width, 100)
            self.assertEqual(img.format, "JPEG")
            
        # Register for Undo
        invoker._undo_stack.append(cmd)
        
        # Test Undo
        print("Testing Undo...")
        invoker.undo()
        self.assertFalse(os.path.exists(expected_output))
        print("Image Optimizer Passed!")

if __name__ == '__main__':
    unittest.main()
