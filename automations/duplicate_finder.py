import os
import hashlib

class DuplicateFinder:
    @staticmethod
    def calculate_file_hash(file_path, chunk_size=1024):
        """Calculate the hash of a file for comparison."""
        hasher = hashlib.md5()
        try:
            with open(file_path, "rb") as file:
                while chunk := file.read(chunk_size):
                    hasher.update(chunk)
        except Exception as e:
            return None
        return hasher.hexdigest()

    @staticmethod
    def find_duplicates(folder_path):
        """Find and return duplicate files in the folder."""
        if not os.path.exists(folder_path):
            return {"error": "Folder does not exist."}

        file_hashes = {}
        duplicates = []

        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = DuplicateFinder.calculate_file_hash(file_path)
                if file_hash:
                    if file_hash in file_hashes:
                        duplicates.append((file_path, file_hashes[file_hash]))
                    else:
                        file_hashes[file_hash] = file_path

        return {"duplicates": duplicates}

    @staticmethod
    def delete_duplicates(duplicates):
        """Delete the duplicate files provided in the list."""
        deleted_files = []
        for duplicate, _ in duplicates:
            try:
                os.remove(duplicate)
                deleted_files.append(duplicate)
            except Exception as e:
                pass  # Handle specific errors if needed
        return deleted_files
