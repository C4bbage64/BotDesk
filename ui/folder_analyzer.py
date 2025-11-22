from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QTextEdit
)
from automations.folder_analyzer import analyze_folder  # Import the folder analyzer logic

class FolderAnalyzerUI(QWidget):
    def __init__(self, folder_path=None):
        super().__init__()
        self.setWindowTitle("Folder Analyzer")
        self.setGeometry(300, 300, 250, 150)

        # Layout
        self.layout = QVBoxLayout()

        # Folder input
        self.folder_label = QLabel("Folder Path:")
        self.folder_input = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_folder)

        # Analyze button
        self.analyze_button = QPushButton("Analyze Folder")
        self.analyze_button.clicked.connect(self.analyze_folder)

        # Log area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)

        # Adding widgets to layout
        self.layout.addWidget(self.folder_label)
        self.layout.addWidget(self.folder_input)
        self.layout.addWidget(self.browse_button)
        self.layout.addWidget(self.analyze_button)
        self.layout.addWidget(self.log_area)

        self.setLayout(self.layout)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_input.setText(folder)

    def analyze_folder(self):
        folder_path = self.folder_input.text().strip()

        if not folder_path:
            self.log_area.append("Error: Please specify a folder path.")
            return

        # Perform analysis and log the result
        try:
            result = analyze_folder(folder_path)
            self.log_area.append(result)
        except Exception as e:
            self.log_area.append(f"Error: {str(e)}")
