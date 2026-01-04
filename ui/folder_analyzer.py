
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QTextEdit, QHBoxLayout
)
from PyQt5.QtCore import Qt
from ui.workers import AnalyzerWorker

class FolderAnalyzerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Folder Analyzer")
        self.worker = None
        self.init_ui()

    def init_ui(self):
        # Layout
        self.layout = QVBoxLayout()

        # Title
        title = QLabel("Folder Analyzer")
        title.setObjectName("PageTitle")
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)

        # Folder input
        folder_layout = QHBoxLayout()
        self.folder_input = QLineEdit()
        self.folder_input.setPlaceholderText("Select a folder to analyze...")
        
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_folder)
        
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(self.browse_button)
        self.layout.addLayout(folder_layout)

        # Analyze button
        self.analyze_button = QPushButton("Analyze Folder")
        self.analyze_button.setObjectName("PrimaryButton")
        self.analyze_button.clicked.connect(self.analyze_folder)
        self.layout.addWidget(self.analyze_button)

        # Log area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setPlaceholderText("Analysis results will appear here...")
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

        self.analyze_button.setEnabled(False)
        self.analyze_button.setText("Analyzing...")
        self.log_area.clear()
        self.log_area.append("Starting analysis... This may take a moment.")
        
        self.worker = AnalyzerWorker(folder_path)
        self.worker.finished.connect(self.on_analyze_finished)
        self.worker.error.connect(self.on_analyze_error)
        self.worker.start()

    def on_analyze_finished(self, result):
        self.analyze_button.setEnabled(True)
        self.analyze_button.setText("Analyze Folder")
        self.log_area.append("\n--- Analysis Complete ---\n")
        self.log_area.append(result)

    def on_analyze_error(self, error_msg):
        self.analyze_button.setEnabled(True)
        self.analyze_button.setText("Analyze Folder")
        self.log_area.append(f"\nError: {error_msg}")

