from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit, QVBoxLayout
from automations.file_organizer import organize_files

class FileOrganizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Organizer")

        # UI elements
        self.folder_label = QLabel("Folder Path:")
        self.folder_input = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.ext_label = QLabel("File Extensions (comma-separated):")
        self.ext_input = QLineEdit()
        self.organize_button = QPushButton("Organize Files")
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_input)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.ext_label)
        layout.addWidget(self.ext_input)
        layout.addWidget(self.organize_button)
        layout.addWidget(self.log_area)
        self.setLayout(layout)

        # Connections
        self.browse_button.clicked.connect(self.browse_folder)
        self.organize_button.clicked.connect(self.organize)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_input.setText(folder)

    def organize(self):
        folder = self.folder_input.text().strip()
        extensions = self.ext_input.text().strip().split(",")
        extensions = [ext.strip() for ext in extensions if ext.strip()]

        if not folder:
            self.log_area.append("Error: Folder path is empty.")
            return

        if not extensions:
            self.log_area.append("Error: No file extensions provided.")
            return

        result = organize_files(folder, extensions)
        for log in result:
            self.log_area.append(log)
