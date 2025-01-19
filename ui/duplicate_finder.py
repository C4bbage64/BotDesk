from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit, QVBoxLayout
from automations.duplicate_finder import find_duplicates

class DuplicateFinder(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Duplicate Finder")

        # UI elements
        self.folder_label = QLabel("Folder Path:")
        self.folder_input = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.find_button = QPushButton("Find Duplicates")
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_input)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.find_button)
        layout.addWidget(self.result_area)
        self.setLayout(layout)

        # Connections
        self.browse_button.clicked.connect(self.browse_folder)
        self.find_button.clicked.connect(self.find)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_input.setText(folder)

    def find(self):
        folder = self.folder_input.text().strip()
        if not folder:
            self.result_area.append("Error: Folder path is empty.")
            return

        duplicates = find_duplicates(folder)
        if duplicates:
            self.result_area.append("Duplicate Files Found:")
            for files in duplicates.values():
                if len(files) > 1:
                    self.result_area.append("\n".join(files))
                    self.result_area.append("-" * 50)
        else:
            self.result_area.append("No duplicate files found.")
