from cryptography.fernet import Fernet
import os

def generate_key(output_path):
    """Generates a key and saves it into a file."""
    key = Fernet.generate_key()
    with open(output_path, "wb") as key_file:
        key_file.write(key)
    return f"Key generated at {output_path}"

def load_key(key_path):
    """Loads the key from the given path."""
    return open(key_path, "rb").read()

def encrypt_file(file_path, key_path):
    """Encrypts a file."""
    key = load_key(key_path)
    f = Fernet(key)
    with open(file_path, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)
    return f"Encrypted {file_path}"

def decrypt_file(file_path, key_path):
    """Decrypts a file."""
    key = load_key(key_path)
    f = Fernet(key)
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(file_path, "wb") as file:
        file.write(decrypted_data)
    return f"Decrypted {file_path}"
