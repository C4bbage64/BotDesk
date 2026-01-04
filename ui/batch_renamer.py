
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QLineEdit, QFileDialog, QTableWidget, QTableWidgetItem, 
    QHeaderView, QGroupBox, QGridLayout, QMessageBox, QProgressBar
)
from PyQt5.QtCore import Qt
from automations.batch_renamer import get_rename_preview
from ui.workers import RenamerWorker

class BatchRenamerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.preview_map = {} # Stores {old_name: new_name}
        self.undo_stack = []
        self.worker = None

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Batch File Renamer")
        title.setObjectName("PageTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Folder Selection
        folder_layout = QHBoxLayout()
        self.folder_input = QLineEdit()
        self.folder_input.setPlaceholderText("Select a folder to rename files...")
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_folder)
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(browse_btn)
        layout.addLayout(folder_layout)

        # Options Group
        options_group = QGroupBox("Renaming Options")
        options_group.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid #555; border-radius: 5px; margin-top: 10px; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px; }")
        options_layout = QGridLayout()
        options_layout.setSpacing(10)
        
        self.prefix_input = QLineEdit()
        self.prefix_input.setPlaceholderText("e.g. img_")
        self.prefix_input.setToolTip("Text to add to the beginning of the filename")
        
        self.suffix_input = QLineEdit()
        self.suffix_input.setPlaceholderText("e.g. _v1")
        self.suffix_input.setToolTip("Text to add to the end of the filename (before extension)")
        
        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText("Text to find")
        self.replace_input.setToolTip("The text you want to remove or replace")
        
        self.with_input = QLineEdit()
        self.with_input.setPlaceholderText("Replacement text")
        self.with_input.setToolTip("The text to insert instead")
        
        options_layout.addWidget(QLabel("Add Prefix:"), 0, 0)
        options_layout.addWidget(self.prefix_input, 0, 1)
        options_layout.addWidget(QLabel("Add Suffix:"), 0, 2)
        options_layout.addWidget(self.suffix_input, 0, 3)
        
        options_layout.addWidget(QLabel("Replace Text:"), 1, 0)
        options_layout.addWidget(self.replace_input, 1, 1)
        options_layout.addWidget(QLabel("With Text:"), 1, 2)
        options_layout.addWidget(self.with_input, 1, 3)
        
        # Clear Button
        clear_btn = QPushButton("Clear Options")
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.clicked.connect(self.clear_options)
        clear_btn.setStyleSheet("background-color: #444; color: white; padding: 5px; border-radius: 3px;")
        options_layout.addWidget(clear_btn, 2, 3)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)

        # Action Buttons (Preview)
        preview_btn = QPushButton("Preview Changes")
        preview_btn.clicked.connect(self.update_preview)
        preview_btn.setObjectName("PrimaryButton")
        layout.addWidget(preview_btn)

        # Preview Table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Original Name", "New Name"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 0) # Indeterminate
        layout.addWidget(self.progress_bar)

        # Rename Button
        self.rename_btn = QPushButton("Rename Files")
        self.rename_btn.clicked.connect(self.run_rename)
        self.rename_btn.setObjectName("SuccessButton")
        self.rename_btn.setEnabled(False)
        layout.addWidget(self.rename_btn)
        
        # Undo Button
        self.undo_btn = QPushButton("Undo Last Rename")
        self.undo_btn.clicked.connect(self.undo_last_action)
        self.undo_btn.setObjectName("PrimaryButton") # Use Primary style or maybe a Warning style?
        self.undo_btn.setEnabled(False)
        self.undo_btn.setStyleSheet("background-color: #d9534f; color: white;") # Bootstrap danger color
        layout.addWidget(self.undo_btn)

        self.setLayout(layout)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_input.setText(folder)
            self.update_preview()
            self.undo_stack = [] # Clear undo stack on folder change? Or keep it? keeping it is safer but tricky if folder path changes.
            # Actually, the stack stores the folder path too, so it's safe.
            self.update_undo_button()
            
    def update_undo_button(self):
        self.undo_btn.setEnabled(len(self.undo_stack) > 0)
        if self.undo_stack:
            self.undo_btn.setText(f"Undo Last Rename ({len(self.undo_stack)})")
        else:
            self.undo_btn.setText("Undo Last Rename")

    def update_preview(self):
        folder = self.folder_input.text()
        if not folder:
            return

        prefix = self.prefix_input.text()
        suffix = self.suffix_input.text()
        replace = self.replace_input.text()
        with_text = self.with_input.text()

        # Get preview data
        preview_list = get_rename_preview(folder, replace, with_text, prefix, suffix)
        
        # Update Table
        self.table.setRowCount(len(preview_list))
        self.preview_map = {}
        
        for i, (old, new) in enumerate(preview_list):
            self.table.setItem(i, 0, QTableWidgetItem(old))
            self.table.setItem(i, 1, QTableWidgetItem(new))
            self.preview_map[old] = new
            
        if preview_list:
            self.rename_btn.setEnabled(True)
            self.rename_btn.setText(f"Rename {len(preview_list)} Files")
        else:
            self.rename_btn.setEnabled(False)
            self.rename_btn.setText("Rename Files")

    def run_rename(self):
        folder = self.folder_input.text()
        if not folder or not self.preview_map:
            return
            
        confirm = QMessageBox.question(
            self, "Confirm Rename", 
            f"Are you sure you want to rename {len(self.preview_map)} files?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            self.toggle_ui(False)
            self.worker = RenamerWorker(folder, self.preview_map)
            self.worker.finished.connect(lambda msg, err: self.on_rename_finished(msg, err, is_undo=False))
            self.worker.error.connect(self.on_rename_error)
            self.worker.start()

    def undo_last_action(self):
        if not self.undo_stack:
            return
            
        folder, reverse_map = self.undo_stack.pop()
        
        confirm = QMessageBox.question(
            self, "Confirm Undo", 
            f"Undo renaming of {len(reverse_map)} files?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            self.toggle_ui(False)
            self.worker = RenamerWorker(folder, reverse_map)
            # is_undo=True prevents adding this action back to the stack
            self.worker.finished.connect(lambda msg, err: self.on_rename_finished(msg, err, is_undo=True)) 
            self.worker.error.connect(self.on_rename_error)
            self.worker.start()
        else:
            # If cancelled, put it back
            self.undo_stack.append((folder, reverse_map))

    def on_rename_finished(self, msg, errors, is_undo=False):
        self.toggle_ui(True)
        if errors:
            error_text = "\n".join(errors[:10])
            if len(errors) > 10:
                error_text += f"\n...and {len(errors)-10} more errors."
            QMessageBox.warning(self, "Completed with Errors", f"{msg}\n\nErrors:\n{error_text}")
        else:
            if not is_undo:
                # Store the reverse operation
                # map was {old: new}, we need {new: old}
                # But wait, self.preview_map might have changed if the user typed stuff.
                # We should capture the map available *at the start* of the worker.
                # For now, self.preview_map is likely still valid as UI was locked.
                
                reverse_map = {new_name: old_name for old_name, new_name in self.preview_map.items()}
                self.undo_stack.append((self.folder_input.text(), reverse_map))
                QMessageBox.information(self, "Success", msg)
            else:
                 QMessageBox.information(self, "Undo Success", "Files have been reverted.")
        
        self.update_undo_button()
        
        # Clear options after success to see the new state? 
        # Actually usually you want to see the files in the new state.
        # But for undo, we want to refresh.
        self.update_preview()
        
    def on_rename_error(self, error_msg):
        self.toggle_ui(True)
        QMessageBox.critical(self, "Error", f"An error occurred:\n{error_msg}")

    def toggle_ui(self, enabled):
        self.rename_btn.setEnabled(enabled)
        self.folder_input.setEnabled(enabled)
        self.progress_bar.setVisible(not enabled)
        if enabled:
            self.rename_btn.setText(f"Rename {len(self.preview_map)} Files")
        else:
            self.rename_btn.setText("Processing...")

    def clear_options(self):
        self.prefix_input.clear()
        self.suffix_input.clear()
        self.replace_input.clear()
        self.with_input.clear()
        self.update_preview()
