from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QLineEdit, QFileDialog, QMessageBox, QProgressBar, QComboBox
)
from PyQt5.QtCore import Qt
from ui.workers import DownloaderWorker
import os

class VideoDownloaderUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.worker = None

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Title
        title = QLabel("YouTube Video Downloader")
        title.setObjectName("PageTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(20)

        # URL Input
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube URL...")
        url_layout.addWidget(QLabel("Video URL:"))
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)

        # Output Path
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Select download folder...")
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_folder)
        path_layout.addWidget(QLabel("Save To:"))
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_btn)
        layout.addLayout(path_layout)

        # Format Selection
        format_layout = QHBoxLayout()
        self.format_combo = QComboBox()
        self.format_combo.addItems(["mp4", "webm", "mkv"])
        format_layout.addWidget(QLabel("Format:"))
        format_layout.addWidget(self.format_combo)
        format_layout.addStretch()
        layout.addLayout(format_layout)
        
        layout.addSpacing(20)

        # Download Button
        self.download_btn = QPushButton("Download Video")
        self.download_btn.setObjectName("PrimaryButton")
        self.download_btn.clicked.connect(self.start_download)
        layout.addWidget(self.download_btn)
        
        # Progress Bar (Indeterminate)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 0)
        layout.addWidget(self.progress_bar)
        
        layout.addStretch()
        self.setLayout(layout)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.path_input.setText(folder)

    def start_download(self):
        url = self.url_input.text()
        path = self.path_input.text()
        fmt = self.format_combo.currentText()
        
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a valid URL.")
            return
        if not path:
            QMessageBox.warning(self, "Error", "Please select an output folder.")
            return
            
        self.toggle_ui(False)
        self.worker = DownloaderWorker(url, path, fmt)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_finished(self, msg):
        self.toggle_ui(True)
        QMessageBox.information(self, "Success", msg)
        self.url_input.clear()

    def on_error(self, err):
        self.toggle_ui(True)
        QMessageBox.critical(self, "Error", f"Download failed:\n{err}")

    def toggle_ui(self, enabled):
        self.download_btn.setEnabled(enabled)
        self.url_input.setEnabled(enabled)
        self.path_input.setEnabled(enabled)
        self.progress_bar.setVisible(not enabled)
