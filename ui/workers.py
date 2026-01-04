from PyQt5.QtCore import QThread, pyqtSignal
from automations.batch_renamer import execute_renames
from automations.folder_analyzer import analyze_folder
from automations.video_downloader import download_video
from automations.file_encryptor import encrypt_file, decrypt_file, generate_key

class RenamerWorker(QThread):
    finished = pyqtSignal(str, list)  # msg, errors
    error = pyqtSignal(str)

    def __init__(self, folder, rename_map):
        super().__init__()
        self.folder = folder
        self.rename_map = rename_map

    def run(self):
        try:
            msg, errors = execute_renames(self.folder, self.rename_map)
            self.finished.emit(msg, errors)
        except Exception as e:
            self.error.emit(str(e))

class AnalyzerWorker(QThread):
    finished = pyqtSignal(object)  # result dict
    error = pyqtSignal(str)

    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path

    def run(self):
        try:
            result = analyze_folder(self.folder_path)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class DownloaderWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, url, output_path, format='mp4'):
        super().__init__()
        self.url = url
        self.output_path = output_path
        self.format = format

    def run(self):
        try:
            msg = download_video(self.url, self.output_path, self.format)
            self.finished.emit(msg)
        except Exception as e:
            self.error.emit(str(e))

class EncryptorWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, mode, file_path, key_path):
        super().__init__()
        self.mode = mode # 'encrypt', 'decrypt', 'generate_key'
        self.file_path = file_path
        self.key_path = key_path

    def run(self):
        try:
            if self.mode == 'encrypt':
                msg = encrypt_file(self.file_path, self.key_path)
            elif self.mode == 'decrypt':
                msg = decrypt_file(self.file_path, self.key_path)
            elif self.mode == 'generate_key':
                msg = generate_key(self.key_path)
            else:
                raise ValueError("Invalid mode")
            self.finished.emit(msg)
        except Exception as e:
            self.error.emit(str(e))
