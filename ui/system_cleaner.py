from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from automations.system_cleaner import clean_temp_files, clean_cache

class SystemCleanerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Cleaner")
        self.setGeometry(400, 300, 600, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("System Cleaner")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Description
        description = QLabel("Clean temporary files and caches to free up space.")
        description.setAlignment(Qt.AlignCenter)
        layout.addWidget(description)

        # Clean Temp Files Button
        self.clean_temp_btn = QPushButton("Clean Temporary Files")
        self.clean_temp_btn.clicked.connect(self.run_clean_temp)
        layout.addWidget(self.clean_temp_btn)

        # Clean Cache Button (Placeholder for now as it requires paths)
        self.clean_cache_btn = QPushButton("Clean Cache (Requires Configuration)")
        self.clean_cache_btn.setEnabled(False) # Disabled until we have a config UI
        self.clean_cache_btn.clicked.connect(self.run_clean_cache)
        layout.addWidget(self.clean_cache_btn)

        # Log Area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)

        self.setLayout(layout)

    def run_clean_temp(self):
        self.log_area.append("Cleaning temporary files...")
        try:
            result = clean_temp_files()
            self.log_area.append(result)
            QMessageBox.information(self, "Success", result)
        except Exception as e:
            self.log_area.append(f"Error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to clean temp files: {str(e)}")

    def run_clean_cache(self):
        # This would need a way to select directories
        pass
