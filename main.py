from controllers import MasterController
from PyQt6.QtWidgets import QApplication
import sys

#lanzar la ventana
app = QApplication(sys.argv)
main = MasterController()
main.display()
sys.exit(app.exec())