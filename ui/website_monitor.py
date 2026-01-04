from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QLineEdit, QFrame, QMessageBox, QGridLayout
)
from PyQt5.QtCore import Qt
from ui.workers import MonitorWorker

class WebsiteMonitorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Title
        title = QLabel("Website Monitor")
        title.setObjectName("PageTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(20)

        # Input Area
        input_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter Website URL (e.g. google.com)...")
        self.check_btn = QPushButton("Check Status")
        self.check_btn.setObjectName("PrimaryButton")
        self.check_btn.clicked.connect(self.check_website)
        
        input_layout.addWidget(self.url_input)
        input_layout.addWidget(self.check_btn)
        layout.addLayout(input_layout)
        
        layout.addSpacing(30)

        # Results Area
        result_frame = QFrame()
        result_frame.setObjectName("Card")
        result_layout = QGridLayout()
        result_frame.setLayout(result_layout)
        
        self.status_label = QLabel("Unknown")
        self.status_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        result_layout.addWidget(QLabel("Status:"), 0, 0)
        result_layout.addWidget(self.status_label, 0, 1)
        
        self.code_label = QLabel("-")
        result_layout.addWidget(QLabel("Response Code:"), 1, 0)
        result_layout.addWidget(self.code_label, 1, 1)
        
        self.time_label = QLabel("- ms")
        result_layout.addWidget(QLabel("Response Time:"), 2, 0)
        result_layout.addWidget(self.time_label, 2, 1)
        
        layout.addWidget(result_frame)
        
        layout.addStretch()
        self.setLayout(layout)

    def check_website(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a URL.")
            return

        self.check_btn.setEnabled(False)
        self.check_btn.setText("Checking...")
        self.status_label.setText("Checking...")
        self.status_label.setStyleSheet("color: black; font-size: 18px; font-weight: bold;")
        
        self.worker = MonitorWorker(url)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_finished(self, result):
        self.check_btn.setEnabled(True)
        self.check_btn.setText("Check Status")
        
        status = result['status']
        code = result['response_code']
        time_ms = result['response_time']
        
        self.status_label.setText(status)
        self.code_label.setText(str(code))
        self.time_label.setText(f"{time_ms} ms")
        
        if "Online" in status:
            self.status_label.setStyleSheet("color: #4CAF50; font-size: 18px; font-weight: bold;")
        else:
            self.status_label.setStyleSheet("color: #F44336; font-size: 18px; font-weight: bold;")

    def on_error(self, err):
        self.check_btn.setEnabled(True)
        self.check_btn.setText("Check Status")
        self.status_label.setText("Error")
        QMessageBox.critical(self, "Error", str(err))
