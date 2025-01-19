from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QTextEdit
)
from automations.duplicate_finder import DuplicateFinder

class DuplicateFinderUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Duplicate Finder")
        self.setGeometry(300, 300, 600, 400)

        # Layout
        self.layout = QVBoxLayout()

        # Folder input
        self.folder_label = QLabel("Folder Path:")
        self.folder_input = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_folder)

        # Find duplicates button
        self.find_button = QPushButton("Find Duplicates")
        self.find_button.clicked.connect(self.find_duplicates)

        # Delete duplicates button
        self.delete_button = QPushButton("Delete Duplicates")
        self.delete_button.setEnabled(False)  # Disabled until duplicates are found
        self.delete_button.clicked.connect(self.delete_duplicates)

        # Log area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)

        # Adding widgets to layout
        self.layout.addWidget(self.folder_label)
        self.layout.addWidget(self.folder_input)
        self.layout.addWidget(self.browse_button)
        self.layout.addWidget(self.find_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.log_area)

        self.setLayout(self.layout)

        # State
        self.duplicates = []

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_input.setText(folder)

    def find_duplicates(self):
        folder_path = self.folder_input.text().strip()
        if not folder_path:
            self.log_area.append("Error: Please specify a folder path.")
            return

        result = DuplicateFinder.find_duplicates(folder_path)

        if "error" in result:
            self.log_area.append(f"Error: {result['error']}")
            return

        self.duplicates = result["duplicates"]

        if self.duplicates:
            self.log_area.append(f"Found {len(self.duplicates)} duplicate files:")
            for duplicate, original in self.duplicates:
                self.log_area.append(f"- Duplicate: {duplicate}\n  Original: {original}")
            self.delete_button.setEnabled(True)
        else:
            self.log_area.append("No duplicate files found.")

    def delete_duplicates(self):
        if not self.duplicates:
            self.log_area.append("Error: No duplicates to delete.")
            return

        deleted_files = DuplicateFinder.delete_duplicates(self.duplicates)
        self.log_area.append(f"Deleted {len(deleted_files)} duplicate files:")
        for file in deleted_files:
            self.log_area.append(f"- {file}")

        self.duplicates = []  # Reset duplicates
        self.delete_button.setEnabled(False)
