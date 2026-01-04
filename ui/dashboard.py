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
        
        # File Management
        self.add_nav_header("File Management")
        self.add_nav_button("File Organizer", 0)
        self.add_nav_button("Duplicate Finder", 1)
        self.add_nav_button("Disk Analyzer", 2)
        self.add_nav_button("Batch Renamer", 5)
        self.add_nav_button("Zip Manager", 6)
        self.add_nav_button("File Encryptor", 9)
        
        # Media Tools
        self.add_nav_header("Media Tools")
        self.add_nav_button("Image Optimizer", 7)
        self.add_nav_button("Video Downloader", 8)
        self.add_nav_button("PDF Tools", 3)
        
        # System & Web
        self.add_nav_header("System & Web")
        self.add_nav_button("System Cleaner", 4)
        self.add_nav_button("Internet Speed Test", 10)
        self.add_nav_button("Website Monitor", 11)
        self.add_nav_button("Web Scraper", 12)

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
        
        from ui.image_optimizer import ImageOptimizerUI
        self.image_optimizer = ImageOptimizerUI()
        
        from ui.video_downloader import VideoDownloaderUI
        self.video_downloader = VideoDownloaderUI()
        
        from ui.file_encryptor import FileEncryptorUI
        self.file_encryptor = FileEncryptorUI()
        
        from ui.speed_test import SpeedTestUI
        self.speed_test = SpeedTestUI()
        
        from ui.website_monitor import WebsiteMonitorUI
        self.website_monitor = WebsiteMonitorUI()
        
        from ui.web_scraper import WebScraperUI
        self.web_scraper = WebScraperUI()

        # Add Tools to Stack
        self.content_area.addWidget(self.file_organizer)
        self.content_area.addWidget(self.duplicate_finder)
        self.content_area.addWidget(self.folder_analyzer)
        self.content_area.addWidget(self.pdf_tools)
        self.content_area.addWidget(self.system_cleaner)
        self.content_area.addWidget(self.batch_renamer)
        self.content_area.addWidget(self.zip_manager)
        self.content_area.addWidget(self.image_optimizer)
        self.content_area.addWidget(self.video_downloader)
        self.content_area.addWidget(self.file_encryptor)
        self.content_area.addWidget(self.speed_test)
        self.content_area.addWidget(self.website_monitor)
        self.content_area.addWidget(self.web_scraper)

        # Add widgets to main layout
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.content_area)

        # Apply Styles
        self.apply_styles()

    def add_nav_header(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-weight: bold; color: #555; margin-top: 10px; margin-bottom: 5px; padding-left: 5px;")
        self.sidebar_layout.addWidget(label)

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
        try:
            with open("assets/style.qss", "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Error loading stylesheet: {e}")

