from PyQt5.QtCore import QThread, pyqtSignal
from automations.batch_renamer import execute_renames
from automations.folder_analyzer import analyze_folder

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
    finished = pyqtSignal(str)  # result text
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
