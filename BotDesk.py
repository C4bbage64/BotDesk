import sys
import os
import shutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
    QFileDialog, QTextEdit
)

class BotDeskApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BotDesk: File Automation")
        self.setGeometry(200, 200, 600, 400)

        # UI elements
        self.folder_label = QLabel("Folder Path:", self)
        self.folder_label.move(20, 20)
        self.folder_input = QLineEdit(self)
        self.folder_input.setGeometry(120, 20, 350, 25)

        self.browse_button = QPushButton("Browse", self)
        self.browse_button.setGeometry(480, 20, 100, 25)
        self.browse_button.clicked.connect(self.browse_folder)

        self.ext_label = QLabel("File Extensions (comma-separated):", self)
        self.ext_label.move(20, 60)
        self.ext_input = QLineEdit(self)
        self.ext_input.setGeometry(220, 60, 250, 25)

        self.organize_button = QPushButton("Organize Files", self)
        self.organize_button.setGeometry(20, 100, 120, 30)
        self.organize_button.clicked.connect(self.organize_files)

        self.quit_button = QPushButton("Quit", self)
        self.quit_button.setGeometry(480, 100, 100, 30)
        self.quit_button.clicked.connect(self.close)

        self.log_area = QTextEdit(self)
        self.log_area.setGeometry(20, 150, 560, 200)
        self.log_area.setReadOnly(True)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_input.setText(folder)

    def organize_files(self):
        folder_path = self.folder_input.text().strip()
        extensions = self.ext_input.text().strip().split(",")
        extensions = [ext.strip() for ext in extensions if ext.strip()]

        if not folder_path or not os.path.exists(folder_path):
            self.log_area.append("Error: Invalid folder path.")
            return

        if not extensions:
            self.log_area.append("Error: Please specify at least one file extension.")
            return

        self.log_area.append(f"Organizing files in: {folder_path}")

        # Call the core file organization function
        self.move_files_to_folders(folder_path, extensions)

    def move_files_to_folders(self, folder_path, extensions):
        try:
            for ext in extensions:
                ext_folder = os.path.join(folder_path, ext)
                if not os.path.exists(ext_folder):
                    os.makedirs(ext_folder)

            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    file_ext = filename.split('.')[-1].lower()
                    if file_ext in extensions:
                        dest_folder = os.path.join(folder_path, file_ext)
                        dest_path = os.path.join(dest_folder, filename)
                        shutil.move(file_path, dest_path)
                        self.log_area.append(f"Moved: {filename} -> {file_ext}/")

            self.log_area.append("File organization completed!")

        except Exception as e:
            self.log_area.append(f"Error: {str(e)}")

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = BotDeskApp()
    main_win.show()
    sys.exit(app.exec_())
