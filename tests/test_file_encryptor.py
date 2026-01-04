import unittest
import os
from automations.file_encryptor import generate_key, encrypt_file, decrypt_file

class TestFileEncryptor(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        self.key_file = "test_key.key"
        self.content = b"Secret Message"
        
        with open(self.test_file, "wb") as f:
            f.write(self.content)

    def tearDown(self):
        if os.path.exists(self.test_file):
            try:
                os.remove(self.test_file)
            except: pass
        if os.path.exists(self.key_file):
            try:
                os.remove(self.key_file)
            except: pass

    def test_encryption_decryption(self):
        # Generate Key
        generate_key(self.key_file)
        self.assertTrue(os.path.exists(self.key_file))

        # Encrypt
        encrypt_file(self.test_file, self.key_file)
        with open(self.test_file, "rb") as f:
            encrypted_content = f.read()
        self.assertNotEqual(encrypted_content, self.content)

        # Decrypt
        decrypt_file(self.test_file, self.key_file)
        with open(self.test_file, "rb") as f:
            decrypted_content = f.read()
        self.assertEqual(decrypted_content, self.content)

if __name__ == '__main__':
    unittest.main()
