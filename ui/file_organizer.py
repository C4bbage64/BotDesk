from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QTextEdit
)
from automations.file_organizer import organize_files

class FileOrganizerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Organizer")
        self.setGeometry(300, 300, 600, 400)

        # Layout
        self.layout = QVBoxLayout()

        # Folder input
        self.folder_label = QLabel("Folder Path:")
        self.folder_input = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_folder)

        # Extensions input
        self.ext_label = QLabel("File Extensions (comma-separated):")
        self.ext_input = QLineEdit()

        # Organize button
        self.organize_button = QPushButton("Organize Files")
        self.organize_button.clicked.connect(self.organize_files)

        # Log area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)

        # Adding widgets to layout
        self.layout.addWidget(self.folder_label)
        self.layout.addWidget(self.folder_input)
        self.layout.addWidget(self.browse_button)
        self.layout.addWidget(self.ext_label)
        self.layout.addWidget(self.ext_input)
        self.layout.addWidget(self.organize_button)
        self.layout.addWidget(self.log_area)

        self.setLayout(self.layout)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_input.setText(folder)

    def organize_files(self):
        folder_path = self.folder_input.text().strip()
        extensions = self.ext_input.text().strip().split(',')
        extensions = [ext.strip() for ext in extensions if ext.strip()]

        if not folder_path:
            self.log_area.append("Error: Please specify a folder path.")
            return

        if not extensions:
            self.log_area.append("Error: Please specify at least one file extension.")
            return

        try:
            result = organize_files(folder_path, extensions)
            self.log_area.append(result)
        except Exception as e:
            self.log_area.append(f"An error occurred: {str(e)}")
