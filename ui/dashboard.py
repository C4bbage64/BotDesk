import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QLabel, QStackedWidget, QTextEdit
)

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BotDesk: Automation Dashboard")
        self.setGeometry(200, 200, 800, 600)

        # Main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Sidebar
        self.sidebar = QVBoxLayout()
        self.sidebar_buttons = []

        # Add automation buttons to the sidebar
        self.add_sidebar_button("File Organizer", self.show_file_organizer)
        self.add_sidebar_button("Bulk Renamer", self.show_bulk_renamer)
        self.add_sidebar_button("Task Scheduler", self.show_task_scheduler)

        main_layout.addLayout(self.sidebar)

        # Main area (Stacked Widget to switch between tasks)
        self.task_area = QStackedWidget()
        main_layout.addWidget(self.task_area)

        # Add placeholder widgets for each task
        self.task_area.addWidget(self.create_placeholder("File Organizer"))
        self.task_area.addWidget(self.create_placeholder("Bulk Renamer"))
        self.task_area.addWidget(self.create_placeholder("Task Scheduler"))

        # Logging area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        main_layout.addWidget(self.log_area)

    def add_sidebar_button(self, name, handler):
        button = QPushButton(name)
        button.clicked.connect(handler)
        self.sidebar.addWidget(button)
        self.sidebar_buttons.append(button)

    def create_placeholder(self, text):
        placeholder = QWidget()
        layout = QVBoxLayout()
        label = QLabel(f"{text} - Coming Soon!")
        layout.addWidget(label)
        placeholder.setLayout(layout)
        return placeholder

    def show_file_organizer(self):
        self.task_area.setCurrentIndex(0)
        self.log_area.append("Switched to File Organizer")

    def show_bulk_renamer(self):
        self.task_area.setCurrentIndex(1)
        self.log_area.append("Switched to Bulk Renamer")

    def show_task_scheduler(self):
        self.task_area.setCurrentIndex(2)
        self.log_area.append("Switched to Task Scheduler")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())
