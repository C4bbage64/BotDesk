import os
import shutil
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog


class FileOrganizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Organizer")

        # UI elements
        self.folder_label = QLabel("Folder Path:", self)
        self.folder_input = QLineEdit(self)
        self.browse_button = QPushButton("Browse", self)
        self.organize_button = QPushButton("Organize Files", self)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_input)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.organize_button)

        self.setLayout(layout)

        # Connections
        self.browse_button.clicked.connect(self.browse_folder)
        self.organize_button.clicked.connect(self.organize_files)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_input.setText(folder)

    def organize_files(self):
        folder_path = self.folder_input.text().strip()

        if not folder_path or not os.path.exists(folder_path):
            print("Error: Invalid folder path.")
            return

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                file_ext = filename.split('.')[-1].lower()
                ext_folder = os.path.join(folder_path, file_ext)
                if not os.path.exists(ext_folder):
                    os.makedirs(ext_folder)
                shutil.move(file_path, os.path.join(ext_folder, filename))

        print("Files Organized Successfully!")
