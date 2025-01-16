import sys
from PyQt5.QtWidgets import QApplication
from ui.dashboard import Dashboard

def main():
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()