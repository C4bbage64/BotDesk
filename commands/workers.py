from PyQt5.QtCore import QThread, pyqtSignal
from core.commands import Command

class CommandWorker(QThread):
    """
    Generic worker to execute any Command in a background thread.
    """
    finished = pyqtSignal(object) # Returns results (success_count, errors) typically
    error = pyqtSignal(str)

    def __init__(self, command: Command):
        super().__init__()
        self.command = command

    def run(self):
        try:
            # Commands should return something useful for the UI
            result = self.command.execute()
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))
