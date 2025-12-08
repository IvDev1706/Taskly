from views.MainView import MainWindow
from PyQt6.QtWidgets import QApplication
import sys

#lanzar la ventana
app = QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec())