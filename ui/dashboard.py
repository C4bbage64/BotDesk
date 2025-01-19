from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel
)
from ui.file_organizer import FileOrganizerUI

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BotDesk Dashboard")
        self.setGeometry(300, 200, 800, 600)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout for the dashboard
        self.layout = QVBoxLayout()

        # Title
        self.title_label = QLabel("Welcome to BotDesk: Your Desktop Automation Hub")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        # Feature buttons
        self.file_organizer_button = QPushButton("File Organizer")
        self.file_organizer_button.clicked.connect(self.open_file_organizer)
        self.layout.addWidget(self.file_organizer_button)

        self.duplicate_finder_button = QPushButton("Duplicate Finder (Coming Soon)")
        self.duplicate_finder_button.setEnabled(False)  # Placeholder for future implementation
        self.layout.addWidget(self.duplicate_finder_button)

        self.folder_analyzer_button = QPushButton("Folder Analyzer (Coming Soon)")
        self.folder_analyzer_button.setEnabled(False)  # Placeholder for future implementation
        self.layout.addWidget(self.folder_analyzer_button)

        self.pdf_tools_button = QPushButton("PDF Tools (Coming Soon)")
        self.pdf_tools_button.setEnabled(False)  # Placeholder for future implementation
        self.layout.addWidget(self.pdf_tools_button)

        self.system_cleaner_button = QPushButton("System Cleaner (Coming Soon)")
        self.system_cleaner_button.setEnabled(False)  # Placeholder for future implementation
        self.layout.addWidget(self.system_cleaner_button)

        # Set the layout
        self.central_widget.setLayout(self.layout)

    def open_file_organizer(self):
        """Opens the File Organizer UI."""
        self.file_organizer_window = FileOrganizerUI()
        self.file_organizer_window.show()