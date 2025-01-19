from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BotDesk Dashboard")
        self.setGeometry(200, 200, 800, 600)

        # Main widget and layout
        self.main_widget = QWidget()
        self.layout = QVBoxLayout()

        # Buttons for each feature
        self.file_organizer_button = QPushButton("File Organizer")
        self.duplicate_finder_button = QPushButton("Duplicate Finder")
        self.folder_analyzer_button = QPushButton("Folder Analyzer")

        # Add buttons to layout
        self.layout.addWidget(QLabel("Welcome to BotDesk! Choose a task:"))
        self.layout.addWidget(self.file_organizer_button)
        self.layout.addWidget(self.duplicate_finder_button)
        self.layout.addWidget(self.folder_analyzer_button)

        # Set layout to main widget
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

        # Connect buttons to actions (to be implemented)
        self.file_organizer_button.clicked.connect(self.open_file_organizer)
        self.duplicate_finder_button.clicked.connect(self.open_duplicate_finder)
        self.folder_analyzer_button.clicked.connect(self.open_folder_analyzer)

    def open_file_organizer(self):
        print("Launching File Organizer...")  # Placeholder action

    def open_duplicate_finder(self):
        print("Launching Duplicate Finder...")  # Placeholder action

    def open_folder_analyzer(self):
        print("Launching Folder Analyzer...")  # Placeholder action
