from PyQt6.QtWidgets import QMessageBox

def info(parent, title: str, msg: str)->None:
    #mensaje
    QMessageBox.information(parent, title, msg, QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)

def warning(parent, title: str, msg: str)->None:
    #mensaje
    QMessageBox.warning(parent, title, msg, QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)
    
def error(parent, title: str, msg: str)->None:
    QMessageBox.critical(parent, title, msg, QMessageBox.StandardButton.Close,QMessageBox.StandardButton.Close)