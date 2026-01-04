from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QFrame, QMessageBox, QGridLayout
)
from PyQt5.QtCore import Qt
from ui.workers import SpeedTestWorker

class SpeedTestUI(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Title
        title = QLabel("Internet Speed Test")
        title.setObjectName("PageTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(30)

        # Dashboard for results
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        
        # Download
        self.download_label = QLabel("0.0 Mbps")
        self.download_label.setStyleSheet("font-size: 24px; color: #4CAF50; font-weight: bold;")
        self.download_label.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(QLabel("Download"), 0, 0, Qt.AlignCenter)
        grid_layout.addWidget(self.download_label, 1, 0, Qt.AlignCenter)
        
        # Upload
        self.upload_label = QLabel("0.0 Mbps")
        self.upload_label.setStyleSheet("font-size: 24px; color: #2196F3; font-weight: bold;")
        self.upload_label.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(QLabel("Upload"), 0, 1, Qt.AlignCenter)
        grid_layout.addWidget(self.upload_label, 1, 1, Qt.AlignCenter)
        
        # Ping
        self.ping_label = QLabel("0 ms")
        self.ping_label.setStyleSheet("font-size: 24px; color: #FF9800; font-weight: bold;")
        self.ping_label.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(QLabel("Ping"), 0, 2, Qt.AlignCenter)
        grid_layout.addWidget(self.ping_label, 1, 2, Qt.AlignCenter)
        
        layout.addLayout(grid_layout)
        
        layout.addSpacing(40)

        # Start Button
        self.start_btn = QPushButton("Start Speed Test")
        self.start_btn.setObjectName("PrimaryButton")
        self.start_btn.setFixedWidth(200)
        self.start_btn.clicked.connect(self.start_test)
        layout.addWidget(self.start_btn, 0, Qt.AlignCenter)
        
        # Status Label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        self.setLayout(layout)

    def start_test(self):
        self.start_btn.setEnabled(False)
        self.start_btn.setText("Testing...")
        self.status_label.setText("Running speed test... This may take a minute.")
        self.reset_labels()
        
        self.worker = SpeedTestWorker()
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_finished(self, results):
        self.start_btn.setEnabled(True)
        self.start_btn.setText("Start Speed Test")
        self.status_label.setText("Test Completed.")
        
        self.download_label.setText(f"{results['download']} Mbps")
        self.upload_label.setText(f"{results['upload']} Mbps")
        self.ping_label.setText(f"{results['ping']} ms")

    def on_error(self, err):
        self.start_btn.setEnabled(True)
        self.start_btn.setText("Start Speed Test")
        self.status_label.setText("Error occurred.")
        QMessageBox.critical(self, "Error", f"Speed test failed:\n{err}")

    def reset_labels(self):
        self.download_label.setText("...")
        self.upload_label.setText("...")
        self.ping_label.setText("...")
