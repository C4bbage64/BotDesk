import os
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QVBoxLayout, QFileDialog

class FileRenamer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bulk Renamer")
        # UI elements
        self.folder_label = QLabel("Folder Path:", self)
        self.folder_input = QLineEdit(self)
        self.rename_pattern_label = QLabel("Rename Pattern (e.g., prefix_###):", self)
        self.rename_pattern_input = QLineEdit(self)
        self.browse_button = QPushButton("Browse", self)
        self.rename_button = QPushButton("Rename Files", self)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_input)
        layout.addWidget(self.rename_pattern_label)
        layout.addWidget(self.rename_pattern_input)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.rename_button)

        self.setLayout(layout)

        # Connections
        self.browse_button.clicked.connect(self.browse_folder)
        self.rename_button.clicked.connect(self.rename_files)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_input.setText(folder)

    def rename_files(self):
        folder_path = self.folder_input.text()
        rename_pattern = self.rename_pattern_input.text().strip()

        if not folder_path or not os.path.exists(folder_path):
            print("Error: Invalid folder path.")
            return

        if not rename_pattern:
            print("Error: Please specify a rename pattern.")
            return

        for idx, filename in enumerate(os.listdir(folder_path)):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                new_name = f"{rename_pattern}_{idx}{os.path.splitext(filename)[1]}"
                new_path = os.path.join(folder_path, new_name)
                os.rename(file_path, new_path)

        print("Files Renamed Succesfully!")