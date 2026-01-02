from PyQt6.QtWidgets import (QWidget, QTabWidget)
from PyQt6.QtGui import QIcon
from .Messages import error
from utils.constants import FNTELEMENT
from utils.config import BASEDIR, VERSION
from database.dbconnection import getInstance
import os

#clase de ventana principal
class MainWindow(QWidget):
    #metodo constructor
    def __init__(self)->None:
        #instancia de padre
        super().__init__()
        
        #hoja de estilos
        try:
            with open(os.path.join(BASEDIR,"assets","styles","main.css"),"r") as styles:
                self.setStyleSheet(styles.read())
                styles.close()
        except OSError as e:
            error(self,"Error",e.strerror)
        
        #componentes
        self.tabBar = QTabWidget(self)
        
        #configuraciones
        self.__config()
        
    #metodos de ventana
    def __config(self)->None:
        #configuracion de ventana
        self.setWindowTitle("Taskly - "+VERSION)
        self.setWindowIcon(QIcon(os.path.join(BASEDIR,"assets","img","taskly-ico.png")))
        self.setFixedSize(600, 400)
        self.setObjectName("main-window")
        
        #configuracion del tabBar
        self.tabBar.setFixedSize(self.size())
        self.tabBar.setFont(FNTELEMENT)
    
    def closeEvent(self, a0):
        #obtener conexion
        con = getInstance()
        #cierre de sesion
        con.close_connection()
        #cierre formal
        super().closeEvent(a0)  