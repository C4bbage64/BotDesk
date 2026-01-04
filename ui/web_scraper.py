from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QLineEdit, QRadioButton, QButtonGroup, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from ui.workers import ScraperWorker

class WebScraperUI(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Title
        title = QLabel("Web Scraper")
        title.setObjectName("PageTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(20)

        # URL Input
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL to scrape...")
        url_layout.addWidget(QLabel("URL:"))
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)
        
        layout.addSpacing(10)

        # Target Selection
        target_layout = QHBoxLayout()
        target_layout.addWidget(QLabel("Extract:"))
        
        self.radio_group = QButtonGroup()
        
        self.rb_links = QRadioButton("Links")
        self.rb_links.setChecked(True)
        self.rb_images = QRadioButton("Images")
        self.rb_text = QRadioButton("Text")
        
        self.radio_group.addButton(self.rb_links)
        self.radio_group.addButton(self.rb_images)
        self.radio_group.addButton(self.rb_text)
        
        target_layout.addWidget(self.rb_links)
        target_layout.addWidget(self.rb_images)
        target_layout.addWidget(self.rb_text)
        target_layout.addStretch()
        
        layout.addLayout(target_layout)
        
        layout.addSpacing(20)

        # Scrape Button
        self.scrape_btn = QPushButton("Scrape Data")
        self.scrape_btn.setObjectName("PrimaryButton")
        self.scrape_btn.clicked.connect(self.run_scraper)
        layout.addWidget(self.scrape_btn)
        
        layout.addSpacing(20)

        # Results Area
        layout.addWidget(QLabel("Results:"))
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        layout.addWidget(self.result_area)

        self.setLayout(layout)

    def run_scraper(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a URL.")
            return

        target = "links"
        if self.rb_images.isChecked():
            target = "images"
        elif self.rb_text.isChecked():
            target = "text"

        self.scrape_btn.setEnabled(False)
        self.scrape_btn.setText("Scraping...")
        self.result_area.clear()
        
        self.worker = ScraperWorker(url, target)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_finished(self, results):
        self.scrape_btn.setEnabled(True)
        self.scrape_btn.setText("Scrape Data")
        
        if not results:
            self.result_area.setText("No data found.")
            return
            
        text = "\n".join(results)
        self.result_area.setText(text)
        QMessageBox.information(self, "Success", f"Found {len(results)} items.")

    def on_error(self, err):
        self.scrape_btn.setEnabled(True)
        self.scrape_btn.setText("Scrape Data")
        QMessageBox.critical(self, "Error", str(err))
