from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QLineEdit, QFileDialog, QListWidget, QTabWidget, QMessageBox
)
from PyQt5.QtCore import Qt
from automations.zip_manager import compress_files, extract_archive
import os

class ZipManagerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Zip & Archive Manager")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_compress_tab(), "Compress Files")
        self.tabs.addTab(self.create_extract_tab(), "Extract Archive")
        layout.addWidget(self.tabs)

        self.setLayout(layout)

    def create_compress_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # File List
        layout.addWidget(QLabel("Selected Files/Folders:"))
        self.file_list = QListWidget()
        layout.addWidget(self.file_list)

        # Buttons to Add/Remove
        btn_layout = QHBoxLayout()
        add_file_btn = QPushButton("Add Files")
        add_file_btn.clicked.connect(self.add_files)
        add_folder_btn = QPushButton("Add Folder")
        add_folder_btn.clicked.connect(self.add_folder)
        remove_btn = QPushButton("Remove Selected")
        remove_btn.clicked.connect(self.remove_selected)
        
        btn_layout.addWidget(add_file_btn)
        btn_layout.addWidget(add_folder_btn)
        btn_layout.addWidget(remove_btn)
        layout.addLayout(btn_layout)

        # Output Path
        layout.addWidget(QLabel("Output Archive Path:"))
        path_layout = QHBoxLayout()
        self.output_zip_input = QLineEdit()
        self.output_zip_input.setPlaceholderText("Save as...")
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_save_zip)
        path_layout.addWidget(self.output_zip_input)
        path_layout.addWidget(browse_btn)
        layout.addLayout(path_layout)

        # Compress Button
        self.compress_btn = QPushButton("Create Archive")
        self.compress_btn.clicked.connect(self.run_compression)
        self.compress_btn.setStyleSheet("background-color: #0e639c; color: white; padding: 10px; font-weight: bold;")
        layout.addWidget(self.compress_btn)
        
        tab.setLayout(layout)
        return tab

    def create_extract_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Archive Selection
        layout.addWidget(QLabel("Select Archive to Extract:"))
        archive_layout = QHBoxLayout()
        self.archive_input = QLineEdit()
        browse_archive_btn = QPushButton("Browse")
        browse_archive_btn.clicked.connect(self.browse_archive)
        archive_layout.addWidget(self.archive_input)
        archive_layout.addWidget(browse_archive_btn)
        layout.addLayout(archive_layout)

        # Destination Selection
        layout.addWidget(QLabel("Extraction Destination:"))
        dest_layout = QHBoxLayout()
        self.extract_dest_input = QLineEdit()
        browse_dest_btn = QPushButton("Browse")
        browse_dest_btn.clicked.connect(self.browse_extract_dest)
        dest_layout.addWidget(self.extract_dest_input)
        dest_layout.addWidget(browse_dest_btn)
        layout.addLayout(dest_layout)

        layout.addStretch()

        # Extract Button
        self.extract_btn = QPushButton("Extract Here")
        self.extract_btn.clicked.connect(self.run_extraction)
        self.extract_btn.setStyleSheet("background-color: #28a745; color: white; padding: 10px; font-weight: bold;")
        layout.addWidget(self.extract_btn)

        tab.setLayout(layout)
        return tab

    # --- Compression Logic ---
    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files")
        if files:
            self.file_list.addItems(files)

    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.file_list.addItem(folder)

    def remove_selected(self):
        for item in self.file_list.selectedItems():
            self.file_list.takeItem(self.file_list.row(item))

    def browse_save_zip(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Archive", "", "Zip Files (*.zip)")
        if path:
            self.output_zip_input.setText(path)

    def run_compression(self):
        items = [self.file_list.item(i).text() for i in range(self.file_list.count())]
        output = self.output_zip_input.text()
        
        if not items:
            QMessageBox.warning(self, "Warning", "Please select files to compress.")
            return
        if not output:
            QMessageBox.warning(self, "Warning", "Please specify an output path.")
            return
            
        msg = compress_files(items, output)
        if "Error" in msg:
            QMessageBox.critical(self, "Error", msg)
        else:
            QMessageBox.information(self, "Success", msg)
            self.file_list.clear()
            self.output_zip_input.clear()

    # --- Extraction Logic ---
    def browse_archive(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Archive", "", "Archives (*.zip *.tar *.gztar *.bztar *.xztar)")
        if path:
            self.archive_input.setText(path)

    def browse_extract_dest(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Destination")
        if folder:
            self.extract_dest_input.setText(folder)

    def run_extraction(self):
        archive = self.archive_input.text()
        dest = self.extract_dest_input.text()
        
        if not archive:
            QMessageBox.warning(self, "Warning", "Please select an archive.")
            return
        if not dest:
            QMessageBox.warning(self, "Warning", "Please select a destination.")
            return
            
        msg = extract_archive(archive, dest)
        if "Error" in msg:
            QMessageBox.critical(self, "Error", msg)
        else:
            QMessageBox.information(self, "Success", msg)
