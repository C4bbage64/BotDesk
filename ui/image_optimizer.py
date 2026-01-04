from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QLineEdit, QFileDialog, QGroupBox, QGridLayout, QMessageBox, 
    QComboBox, QSpinBox, QProgressBar
)
from PyQt5.QtCore import Qt
from core.commands import CommandInvoker
from commands.image_commands import BatchOptimizeCommand
from commands.workers import CommandWorker

class ImageOptimizerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.invoker = CommandInvoker()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Image Optimizer")
        title.setObjectName("PageTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # File Selection (Single file or Folder)
        # Simplified: Folder Selection
        folder_layout = QHBoxLayout()
        self.folder_input = QLineEdit()
        self.folder_input.setPlaceholderText("Select a folder with images...")
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_folder)
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(browse_btn)
        layout.addLayout(folder_layout)

        # Settings Group
        settings_group = QGroupBox("Optimization Settings")
        settings_layout = QGridLayout()
        
        # Max Width
        settings_layout.addWidget(QLabel("Max Width (px):"), 0, 0)
        self.width_spin = QSpinBox()
        self.width_spin.setRange(0, 8000)
        self.width_spin.setValue(0) # 0 means No Resize
        self.width_spin.setSpecialValueText("Original Size")
        settings_layout.addWidget(self.width_spin, 0, 1)

        # Quality
        settings_layout.addWidget(QLabel("Quality (1-100):"), 0, 2)
        self.quality_spin = QSpinBox()
        self.quality_spin.setRange(1, 100)
        self.quality_spin.setValue(85)
        settings_layout.addWidget(self.quality_spin, 0, 3)

        # Convert Format
        settings_layout.addWidget(QLabel("Convert To:"), 1, 0)
        self.format_combo = QComboBox()
        self.format_combo.addItems(["Keep Original", "JPG", "PNG", "WEBP"])
        settings_layout.addWidget(self.format_combo, 1, 1)

        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 0) 
        layout.addWidget(self.progress_bar)

        # Action Buttons
        btn_layout = QHBoxLayout()
        
        self.run_btn = QPushButton("Optimize Images")
        self.run_btn.setObjectName("SuccessButton")
        self.run_btn.clicked.connect(self.run_optimization)
        
        self.undo_btn = QPushButton("Undo")
        self.undo_btn.setObjectName("PrimaryButton")
        self.undo_btn.setStyleSheet("background-color: #d9534f; color: white;")
        self.undo_btn.setEnabled(False)
        self.undo_btn.clicked.connect(self.undo_last)

        btn_layout.addWidget(self.run_btn)
        btn_layout.addWidget(self.undo_btn)
        layout.addLayout(btn_layout)
        
        layout.addStretch()
        self.setLayout(layout)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_input.setText(folder)

    def run_optimization(self):
        folder = self.folder_input.text()
        if not folder:
            QMessageBox.warning(self, "Input Error", "Please select a folder.")
            return

        import os
        # Gather images
        valid_exts = ('.jpg', '.jpeg', '.png', '.webp', '.bmp')
        files = [
            os.path.join(folder, f) for f in os.listdir(folder) 
            if f.lower().endswith(valid_exts)
        ]
        
        if not files:
            QMessageBox.warning(self, "No Images", "No valid images found in folder.")
            return

        # Prepare Command
        max_width = self.width_spin.value() if self.width_spin.value() > 0 else None
        fmt_selection = self.format_combo.currentText()
        convert_to = None if fmt_selection == "Keep Original" else fmt_selection.lower()

        command = BatchOptimizeCommand(
            file_paths=files,
            output_dir=None, # In-place (suffix)
            quality=self.quality_spin.value(),
            max_width=max_width,
            format=convert_to
        )
        
        # Run in worker
        self.toggle_ui(False)
        self.worker = CommandWorker(command)
        self.worker.finished.connect(lambda res: self.on_finished(res, command))
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_finished(self, result, command):
        self.toggle_ui(True)
        count, errors = result
        
        # Register command with invoker
        self.invoker.execute_command(command) # This logically adds it to stack
        self.update_undo_btn()

        if errors:
             QMessageBox.warning(self, "Finished with Errors", f"Optimized {count} images.\nErrors: {len(errors)}")
        else:
             QMessageBox.information(self, "Success", f"Successfully optimized {count} images.")

    def on_error(self, err):
        self.toggle_ui(True)
        QMessageBox.critical(self, "Error", str(err))

    def undo_last(self):
        if self.invoker.undo():
            self.update_undo_btn()
            QMessageBox.information(self, "Undo", "Last batch optimization undone (files reversed).")
        else:
            QMessageBox.warning(self, "Undo", "Nothing to undo.")

    def update_undo_btn(self):
        self.undo_btn.setEnabled(self.invoker.can_undo())

    def toggle_ui(self, enabled):
        self.run_btn.setEnabled(enabled)
        self.folder_input.setEnabled(enabled)
        self.progress_bar.setVisible(not enabled)

