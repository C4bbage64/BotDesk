from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, 
    QTextEdit, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView,
    QTabWidget, QMenu, QMessageBox, QProgressBar
)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from ui.workers import AnalyzerWorker
import os

class FolderAnalyzerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        # Layout
        layout = QVBoxLayout()

        # Title
        title = QLabel("Disk Space Analyzer")
        title.setObjectName("PageTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Folder input
        folder_layout = QHBoxLayout()
        self.folder_input = QLineEdit()
        self.folder_input.setPlaceholderText("Select drive or folder to analyze (e.g. C:/)...")
        
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_folder)
        
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(browse_button)
        layout.addLayout(folder_layout)

        # Analyze button
        self.analyze_button = QPushButton("Analyze Usage")
        self.analyze_button.setObjectName("PrimaryButton")
        self.analyze_button.clicked.connect(self.analyze_folder)
        layout.addWidget(self.analyze_button)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 0) # Indeterminate initially
        layout.addWidget(self.progress_bar)

        # Summary Label
        self.summary_label = QLabel("Ready to analyze.")
        self.summary_label.setAlignment(Qt.AlignCenter)
        self.summary_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px;")
        layout.addWidget(self.summary_label)

        # Tabs for Results
        self.tabs = QTabWidget()
        
        self.files_table = self.create_table(["File Path", "Size (MB)"])
        self.folders_table = self.create_table(["Folder Path", "Size (MB)"])
        
        self.tabs.addTab(self.files_table, "Largest Files")
        self.tabs.addTab(self.folders_table, "Largest Folders")
        
        layout.addWidget(self.tabs)

        self.setLayout(layout)

    def create_table(self, headers):
        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        table.setContextMenuPolicy(Qt.CustomContextMenu)
        table.customContextMenuRequested.connect(lambda pos: self.open_menu(pos, table))
        return table

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_input.setText(folder)

    def analyze_folder(self):
        folder_path = self.folder_input.text().strip()

        if not folder_path:
             QMessageBox.warning(self, "Error", "Please specify a folder path.")
             return

        self.toggle_ui(False)
        self.progress_bar.setVisible(True)
        self.summary_label.setText("Analyzing... This may take a while for large drives.")
        
        self.worker = AnalyzerWorker(folder_path)
        self.worker.finished.connect(self.on_analyze_finished)
        self.worker.progress.connect(self.on_progress)
        self.worker.error.connect(self.on_analyze_error)
        self.worker.start()
        
    def on_progress(self, count):
        self.summary_label.setText(f"Scanning... Found {count} files")

    def on_analyze_finished(self, result):
        self.toggle_ui(True)
        self.progress_bar.setVisible(False)
        
        # Update Summary
        size_gb = result['total_size'] / (1024**3)
        self.summary_label.setText(
            f"Total Size: {size_gb:.2f} GB | "
            f"Files: {result['total_files']} | "
            f"Folders: {result['total_folders']}"
        )
        
        # Populate Tables
        self.populate_table(self.files_table, result['top_files'])
        self.populate_table(self.folders_table, result['top_folders'])

    def populate_table(self, table, data_list):
        table.setRowCount(0)
        table.setRowCount(len(data_list))
        for i, (path, size) in enumerate(data_list):
            size_mb = size / (1024*1024)
            table.setItem(i, 0, QTableWidgetItem(path))
            table.setItem(i, 1, QTableWidgetItem(f"{size_mb:.2f} MB"))

    def on_analyze_error(self, error_msg):
        self.toggle_ui(True)
        self.progress_bar.setVisible(False)
        self.summary_label.setText("Analysis Failed.")
        QMessageBox.critical(self, "Error", str(error_msg))

    def toggle_ui(self, enabled):
        self.analyze_button.setEnabled(enabled)
        self.folder_input.setEnabled(enabled)
        if not enabled:
            self.analyze_button.setText("Scanning...")
        else:
            self.analyze_button.setText("Analyze Usage")

    def open_menu(self, position, table):
        menu = QMenu()
        open_action = menu.addAction("Open Location")
        action = menu.exec_(table.viewport().mapToGlobal(position))
        
        if action == open_action:
            row = table.currentRow()
            path_item = table.item(row, 0)
            if path_item:
                file_path = path_item.text()
                folder = os.path.dirname(file_path) if os.path.isfile(file_path) else file_path
                QDesktopServices.openUrl(QUrl.fromLocalFile(folder))
