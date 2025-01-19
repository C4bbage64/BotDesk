import sys
from PyQt5.QtWidgets import QApplication
from ui.dashboard import Dashboard

def main():
    # Create the Qt application
    app = QApplication(sys.argv)

    # Initialize the dashboard
    window = Dashboard()
    window.show()

    # Start the Qt event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()