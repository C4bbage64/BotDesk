import os
import time
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog
from PyQt5.QtCore import QTimer

class TaskScheduler(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Scheduler")

        # UI elements
        self.folder_label = QLabel("Folder Path:", self)
        self.folder_input = QLineEdit(self)
        self.schedule_time_label = QLabel("Time Interval (seconds):", self)
        self.schedule_time_input = QLineEdit(self)
        self.browse_button = QPushButton("Browse", self)
        self.schedule_button = QPushButton("Schedule Task", self)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_input)
        layout.addWidget(self.schedule_time_label)
        layout.addWidget(self.schedule_time_input)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.schedule_button)

        self.setLayout(layout)

        # Connections
        self.browse_button.clicked.connect(self.browse_folder)
        self.schedule_button.clicked.connect(self.schedule_task)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_input.setText(folder)

    def schedule_task(self):
        folder_path = self.folder_input.text().strip()
        interval = int(self.schedule_time_input.text().strip())

        if not folder_path or not os.path.exists(folder_path):
            print("Error: Invalid folder path.")
            return

        if not interval:
            print("Error: Please specify a valid time interval.")
            return

        # Schedule task with timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.organize_files(folder_path))
        self.timer.start(interval * 1000)  # Convert to milliseconds
        print(f"Task scheduled to run every {interval} seconds.")

    def organize_files(self, folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                file_ext = filename.split('.')[-1].lower()
                ext_folder = os.path.join(folder_path, file_ext)
                if not os.path.exists(ext_folder):
                    os.makedirs(ext_folder)
                shutil.move(file_path, os.path.join(ext_folder, filename))

        print(f"Task executed on {time.strftime('%Y-%m-%d %H:%M:%S')}")
