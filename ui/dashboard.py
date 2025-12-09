from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel, QStackedWidget, QFrame
)
from PyQt5.QtCore import Qt
from ui.file_organizer import FileOrganizerUI
from ui.duplicate_finder import DuplicateFinderUI
from ui.folder_analyzer import FolderAnalyzerUI
from ui.pdf_tools import PDFToolsUI
from ui.system_cleaner import SystemCleanerUI
from ui.batch_renamer import BatchRenamerUI
from ui.zip_manager import ZipManagerUI

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BotDesk Automation")
        self.setGeometry(100, 100, 1000, 700)
        
        # Main Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(0, 20, 0, 20)
        self.sidebar_layout.setSpacing(10)
        self.sidebar.setFixedWidth(250)

        # Sidebar Title
        self.title_label = QLabel("BotDesk")
        self.title_label.setObjectName("SidebarTitle")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.sidebar_layout.addWidget(self.title_label)
        
        self.sidebar_layout.addSpacing(20)

        # Navigation Buttons
        self.nav_buttons = []
        self.add_nav_button("File Organizer", 0)
        self.add_nav_button("Duplicate Finder", 1)
        self.add_nav_button("Folder Analyzer", 2)
        self.add_nav_button("PDF Tools", 3)
        self.add_nav_button("System Cleaner", 4)
        self.add_nav_button("Batch Renamer", 5)
        self.add_nav_button("Zip Manager", 6)

        self.sidebar_layout.addStretch()
        
        # Version/Footer
        self.version_label = QLabel("v1.0.0")
        self.version_label.setObjectName("VersionLabel")
        self.version_label.setAlignment(Qt.AlignCenter)
        self.sidebar_layout.addWidget(self.version_label)

        # Content Area
        self.content_area = QStackedWidget()
        
        # Initialize Tools
        self.file_organizer = FileOrganizerUI()
        self.duplicate_finder = DuplicateFinderUI()
        self.folder_analyzer = FolderAnalyzerUI()
        self.pdf_tools = PDFToolsUI()
        self.system_cleaner = SystemCleanerUI()
        self.batch_renamer = BatchRenamerUI()
        self.zip_manager = ZipManagerUI()

        # Add Tools to Stack
        self.content_area.addWidget(self.file_organizer)
        self.content_area.addWidget(self.duplicate_finder)
        self.content_area.addWidget(self.folder_analyzer)
        self.content_area.addWidget(self.pdf_tools)
        self.content_area.addWidget(self.system_cleaner)
        self.content_area.addWidget(self.batch_renamer)
        self.content_area.addWidget(self.zip_manager)

        # Add widgets to main layout
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.content_area)

        # Apply Styles
        self.apply_styles()

    def add_nav_button(self, text, index):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.clicked.connect(lambda: self.switch_page(index, btn))
        self.sidebar_layout.addWidget(btn)
        self.nav_buttons.append(btn)
        
        # Select first button by default
        if index == 0:
            btn.setChecked(True)

    def switch_page(self, index, sender_btn):
        self.content_area.setCurrentIndex(index)
        
        # Update button states
        for btn in self.nav_buttons:
            btn.setChecked(False)
        sender_btn.setChecked(True)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QFrame#Sidebar {
                background-color: #252526;
                border-right: 1px solid #333;
            }
            QLabel#SidebarTitle {
                color: #ffffff;
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
            }
            QLabel#VersionLabel {
                color: #888888;
                font-size: 12px;
            }
            QPushButton {
                background-color: transparent;
                color: #cccccc;
                border: none;
                padding: 15px 20px;
                text-align: left;
                font-size: 14px;
                border-left: 4px solid transparent;
            }
            QPushButton:hover {
                background-color: #2a2d2e;
                color: #ffffff;
            }
            QPushButton:checked {
                background-color: #37373d;
                color: #ffffff;
                border-left: 4px solid #007acc;
            }
            QWidget {
                color: #ffffff;
                font-family: 'Segoe UI', sans-serif;
            }
            QLineEdit {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555;
                padding: 8px;
                border-radius: 4px;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #cccccc;
                border: 1px solid #333;
                border-radius: 4px;
            }
            /* Specific styles for tool buttons inside pages */
            QPushButton[text="Browse"], QPushButton[text="Organize Files"], 
            QPushButton[text="Find Duplicates"], QPushButton[text="Delete Duplicates"],
            QPushButton[text="Analyze Folder"], QPushButton[text="Merge PDFs"],
            QPushButton[text="Split PDF"], QPushButton[text="Extract Text"],
            QPushButton[text="Clean Temporary Files"] {
                background-color: #0e639c;
                color: white;
                border-radius: 4px;
                padding: 8px 16px;
                border: none;
            }
            QPushButton[text="Browse"]:hover, QPushButton[text="Organize Files"]:hover,
            QPushButton[text="Find Duplicates"]:hover, QPushButton[text="Delete Duplicates"]:hover,
            QPushButton[text="Analyze Folder"]:hover, QPushButton[text="Merge PDFs"]:hover,
            QPushButton[text="Split PDF"]:hover, QPushButton[text="Extract Text"]:hover,
            QPushButton[text="Clean Temporary Files"]:hover {
                background-color: #1177bb;
            }
            QPushButton:disabled {
                background-color: #3a3d41;
                color: #888888;
            }
        """)
