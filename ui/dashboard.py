from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QStackedWidget, QTextEdit
from ui.file_organizer import FileOrganizer
from ui.duplicate_finder import DuplicateFinder
from ui.folder_analyzer import FolderAnalyzer

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BotDesk: Desktop Automation")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout()
        central_widget.setLayout(layout)

        # Sidebar for navigation
        self.sidebar = QVBoxLayout()
        layout.addLayout(self.sidebar, 1)

        # Task area (main content)
        self.task_area = QStackedWidget()
        layout.addWidget(self.task_area, 4)

        # Log area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area, 1)

        # Add sidebar buttons
        self.add_sidebar_button("File Organizer", self.show_file_organizer)
        self.add_sidebar_button("Duplicate Finder", self.show_duplicate_finder)
        self.add_sidebar_button("Folder Analyzer", self.show_folder_analyzer)

        # Add modules to the stacked widget
        self.file_organizer = FileOrganizer()
        self.duplicate_finder = DuplicateFinder()
        self.folder_analyzer = FolderAnalyzer()

        self.task_area.addWidget(self.file_organizer)
        self.task_area.addWidget(self.duplicate_finder)
        self.task_area.addWidget(self.folder_analyzer)

    def add_sidebar_button(self, label, callback):
        button = QPushButton(label)
        button.clicked.connect(callback)
        self.sidebar.addWidget(button)

    def show_file_organizer(self):
        self.task_area.setCurrentWidget(self.file_organizer)
        self.log_area.append("Switched to File Organizer")

    def show_duplicate_finder(self):
        self.task_area.setCurrentWidget(self.duplicate_finder)
        self.log_area.append("Switched to Duplicate Finder")

    def show_folder_analyzer(self):
        self.task_area.setCurrentWidget(self.folder_analyzer)
        self.log_area.append("Switched to Folder Analyzer")
