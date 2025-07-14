from PyQt6.QtWidgets import QMessageBox

def warning(parent, title: str, msg: str)->None:
    #mensaje
    QMessageBox.warning(parent, title, msg, QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)