from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QTextEdit
)
from automations.pdf_tools import merge_pdfs, split_pdfs, extract_text_from_pdf

class PDFToolsUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Tools")
        self.setGeometry(300, 300, 600, 400)

        self.layout = QVBoxLayout()

        # File input
        self.file_label = QLabel("PDF File:")
        self.file_input = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_file)

        # Merge PDFs
        self.merge_button = QPushButton("Merge PDFs (Coming Soon)")
        self.merge_button.setEnabled(False)  # Placeholder

        # Split PDFs
        self.split_button = QPushButton("Split PDF")
        self.split_button.clicked.connect(self.split_pdf)

        # Extract text from PDF
        self.extract_text_button = QPushButton("Extract Text")
        self.extract_text_button.clicked.connect(self.extract_text)

        # Log area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)

        # Add widgets to layout
        self.layout.addWidget(self.file_label)
        self.layout.addWidget(self.file_input)
        self.layout.addWidget(self.browse_button)
        self.layout.addWidget(self.merge_button)
        self.layout.addWidget(self.split_button)
        self.layout.addWidget(self.extract_text_button)
        self.layout.addWidget(self.log_area)

        self.setLayout(self.layout)

    def browse_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)")
        if file:
            self.file_input.setText(file)

    def split_pdf(self):
        input_file = self.file_input.text().strip()
        if not input_file:
            self.log_area.append("Error: Please specify a PDF file.")
            return
        result = split_pdfs(input_file)
        self.log_area.append(result)

    def extract_text(self):
        input_file = self.file_input.text().strip()
        if not input_file:
            self.log_area.append("Error: Please specify a PDF file.")
            return
        result = extract_text_from_pdf(input_file)
        self.log_area.append("Extracted Text:\n" + result)
