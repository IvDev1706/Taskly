from views.MainView import MainWindow
from PyQt6.QtWidgets import QApplication
from database.dbconnection import start_db
import sys

#lanzar la ventana
start_db()
app = QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec())