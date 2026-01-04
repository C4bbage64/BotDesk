from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QLineEdit, QFileDialog, QMessageBox, QTabWidget, QGroupBox, QGridLayout
)
from PyQt5.QtCore import Qt
from ui.workers import EncryptorWorker
import os

class FileEncryptorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.worker = None

    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel("File Encryptor & Decryptor")
        title.setObjectName("PageTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.tabs = QTabWidget()
        
        # Tab 1: Key Generation
        self.key_gen_tab = QWidget()
        self.init_key_gen_tab()
        self.tabs.addTab(self.key_gen_tab, "Generate Key")
        
        # Tab 2: Encrypt/Decrypt
        self.crypto_tab = QWidget()
        self.init_crypto_tab()
        self.tabs.addTab(self.crypto_tab, "Encrypt / Decrypt")
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def init_key_gen_tab(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        info = QLabel("Generate a secure key file to encrypt your data.\nKeep this key safe! Without it, you cannot decrypt your files.")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)
        
        self.key_out_path = QLineEdit()
        self.key_out_path.setPlaceholderText("Select location to save key...")
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(lambda: self.browse_save_file(self.key_out_path, "Key Files (*.key)"))
        
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.key_out_path)
        h_layout.addWidget(browse_btn)
        layout.addLayout(h_layout)
        
        gen_btn = QPushButton("Generate New Key")
        gen_btn.setObjectName("SuccessButton")
        gen_btn.clicked.connect(self.generate_key)
        layout.addWidget(gen_btn)
        
        self.key_gen_tab.setLayout(layout)

    def init_crypto_tab(self):
        layout = QVBoxLayout()
        
        # File Selection
        layout.addWidget(QLabel("Target File:"))
        file_layout = QHBoxLayout()
        self.target_file = QLineEdit()
        browse_file_btn = QPushButton("Browse")
        browse_file_btn.clicked.connect(lambda: self.browse_file(self.target_file))
        file_layout.addWidget(self.target_file)
        file_layout.addWidget(browse_file_btn)
        layout.addLayout(file_layout)
        
        # Key Selection
        layout.addWidget(QLabel("Key File:"))
        key_layout = QHBoxLayout()
        self.key_file = QLineEdit()
        browse_key_btn = QPushButton("Browse")
        browse_key_btn.clicked.connect(lambda: self.browse_file(self.key_file, "Key Files (*.key)"))
        key_layout.addWidget(self.key_file)
        key_layout.addWidget(browse_key_btn)
        layout.addLayout(key_layout)
        
        layout.addSpacing(20)
        
        # Buttons
        btn_layout = QHBoxLayout()
        encrypt_btn = QPushButton("Encrypt File")
        encrypt_btn.setObjectName("PrimaryButton")
        encrypt_btn.clicked.connect(lambda: self.run_crypto('encrypt'))
        
        decrypt_btn = QPushButton("Decrypt File")
        decrypt_btn.setObjectName("SuccessButton") # Maybe different style?
        decrypt_btn.clicked.connect(lambda: self.run_crypto('decrypt'))
        
        btn_layout.addWidget(encrypt_btn)
        btn_layout.addWidget(decrypt_btn)
        layout.addLayout(btn_layout)
        
        layout.addStretch()
        self.crypto_tab.setLayout(layout)

    def browse_file(self, line_edit, filter="All Files (*)"):
        path, _ = QFileDialog.getOpenFileName(self, "Select File", "", filter)
        if path:
            line_edit.setText(path)

    def browse_save_file(self, line_edit, filter="All Files (*)"):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", "", filter)
        if path:
            line_edit.setText(path)

    def generate_key(self):
        path = self.key_out_path.text()
        if not path:
            QMessageBox.warning(self, "Error", "Please select a save location.")
            return
            
        self.worker = EncryptorWorker('generate_key', None, path)
        self.worker.finished.connect(self.on_success)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def run_crypto(self, mode):
        file_path = self.target_file.text()
        key_path = self.key_file.text()
        
        if not file_path or not os.path.exists(file_path):
             QMessageBox.warning(self, "Error", "Invalid file path.")
             return
        if not key_path or not os.path.exists(key_path):
             QMessageBox.warning(self, "Error", "Invalid key path.")
             return
             
        self.worker = EncryptorWorker(mode, file_path, key_path)
        self.worker.finished.connect(self.on_success)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_success(self, msg):
        QMessageBox.information(self, "Success", msg)

    def on_error(self, err):
        QMessageBox.critical(self, "Error", f"Operation failed:\n{err}")
