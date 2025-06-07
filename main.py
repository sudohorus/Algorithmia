import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def main():
    """ entry Point da aplicação """
    app = QApplication(sys.argv)

    app.setApplicationName("Algorithmia")
    app.setApplicationVersion("0.1.0")
    app.setOrganizationName("Algorithmia")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

