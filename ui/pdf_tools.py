from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QTextEdit,
    QTabWidget, QHBoxLayout, QListWidget, QMessageBox
)
from PyQt5.QtCore import Qt
from automations.pdf_tools import merge_pdfs, split_pdfs, extract_text_from_pdf
import os

class PDFToolsUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Tools")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("PDF Toolkit")
        title.setObjectName("PageTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Tabs
        self.tabs = QTabWidget()
        
        # Tab 1: Single File Actions (Split / Extract)
        self.single_tab = QWidget()
        self.init_single_tab()
        self.tabs.addTab(self.single_tab, "Split & Extract")
        
        # Tab 2: Merge Actions
        self.merge_tab = QWidget()
        self.init_merge_tab()
        self.tabs.addTab(self.merge_tab, "Merge PDFs")
        
        layout.addWidget(self.tabs)
        
        # Log Area (Shared)
        layout.addWidget(QLabel("Output Log:"))
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMaximumHeight(150)
        layout.addWidget(self.log_area)

        self.setLayout(layout)

    def init_single_tab(self):
        layout = QVBoxLayout()
        
        # File input
        file_layout = QHBoxLayout()
        self.single_file_input = QLineEdit()
        self.single_file_input.setPlaceholderText("Select a PDF file...")
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(lambda: self.browse_file(self.single_file_input))
        file_layout.addWidget(self.single_file_input)
        file_layout.addWidget(browse_btn)
        layout.addLayout(file_layout)
        
        layout.addSpacing(20)

        # Actions
        split_btn = QPushButton("Split PDF into Pages")
        split_btn.setObjectName("PrimaryButton")
        split_btn.clicked.connect(self.split_pdf)
        layout.addWidget(split_btn)
        
        extract_btn = QPushButton("Extract Text from PDF")
        extract_btn.clicked.connect(self.extract_text)
        layout.addWidget(extract_btn)
        
        layout.addStretch()
        self.single_tab.setLayout(layout)

    def init_merge_tab(self):
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("PDF Files to Merge:"))
        
        # List and Controls
        h_layout = QHBoxLayout()
        
        self.file_list = QListWidget()
        h_layout.addWidget(self.file_list)
        
        btn_layout = QVBoxLayout()
        add_btn = QPushButton("Add PDF(s)")
        add_btn.clicked.connect(self.add_pdfs_to_merge)
        
        remove_btn = QPushButton("Remove Selected")
        remove_btn.clicked.connect(self.remove_selected_pdf)
        
        clear_btn = QPushButton("Clear List")
        clear_btn.clicked.connect(self.file_list.clear)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(remove_btn)
        btn_layout.addWidget(clear_btn)
        btn_layout.addStretch()
        
        h_layout.addLayout(btn_layout)
        layout.addLayout(h_layout)

        # Output File
        layout.addWidget(QLabel("Output Filename:"))
        out_layout = QHBoxLayout()
        self.merge_out = QLineEdit()
        self.merge_out.setPlaceholderText("Select output location...")
        browse_out = QPushButton("Browse")
        browse_out.clicked.connect(self.browse_save)
        out_layout.addWidget(self.merge_out)
        out_layout.addWidget(browse_out)
        layout.addLayout(out_layout)
        
        layout.addSpacing(10)
        
        merge_btn = QPushButton("Merge PDFs")
        merge_btn.setObjectName("SuccessButton")
        merge_btn.clicked.connect(self.run_merge)
        layout.addWidget(merge_btn)
        
        self.merge_tab.setLayout(layout)

    def browse_file(self, line_edit):
        path, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF Files (*.pdf)")
        if path:
            line_edit.setText(path)

    def add_pdfs_to_merge(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDFs", "", "PDF Files (*.pdf)")
        if files:
            self.file_list.addItems(files)

    def remove_selected_pdf(self):
        for item in self.file_list.selectedItems():
            self.file_list.takeItem(self.file_list.row(item))

    def browse_save(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Merged PDF", "", "PDF Files (*.pdf)")
        if path:
             self.merge_out.setText(path)

    def split_pdf(self):
        input_file = self.single_file_input.text().strip()
        if not input_file or not os.path.exists(input_file):
            self.log("Error: Invalid input file.")
            return
        
        try:
             # Ideally use a worker here too
             result = split_pdfs(input_file)
             self.log(result)
             QMessageBox.information(self, "Success", "PDF Split Successfully")
        except Exception as e:
             self.log(f"Error splitting PDF: {e}")
             QMessageBox.critical(self, "Error", str(e))

    def extract_text(self):
        input_file = self.single_file_input.text().strip()
        if not input_file or not os.path.exists(input_file):
            self.log("Error: Invalid input file.")
            return

        try:
             result = extract_text_from_pdf(input_file)
             self.log("--- Extracted Text ---")
             self.log(result[:1000] + "..." if len(result) > 1000 else result)
             self.log("----------------------")
        except Exception as e:
             self.log(f"Error extracting text: {e}")

    def run_merge(self):
        count = self.file_list.count()
        if count < 2:
            QMessageBox.warning(self, "Warning", "Please add at least 2 PDF files to merge.")
            return
        
        output_file = self.merge_out.text().strip()
        if not output_file:
             QMessageBox.warning(self, "Warning", "Please specify an output file.")
             return
             
        files = [self.file_list.item(i).text() for i in range(count)]
        
        try:
            self.log("Merging PDFs...")
            result = merge_pdfs(files, output_file)
            self.log(result)
            QMessageBox.information(self, "Success", "PDFs Merged Successfully")
        except Exception as e:
            self.log(f"Error merging PDFs: {e}")
            QMessageBox.critical(self, "Error", str(e))

    def log(self, message):
        self.log_area.append(message)
