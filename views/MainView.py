from PyQt6.QtWidgets import (QWidget, QTabWidget)
from .TaskView import TaskTab
from .ProjectView import ProjectTab
from utils.variables import FNTELEMENT
from database.dbconnection import DBConector

#clase de ventana principal
class MainWindow(QWidget):
    #metodo constructor
    def __init__(self)->None:
        #instancia de padre
        super().__init__()
        
        #hoja de estilos
        try:
            with open("C:\\Users\\Ivan Cadena\\ProyectosPython\\Topicos\\Taskly\\assets\\styles\\main.css","r") as styles:
                self.setStyleSheet(styles.read())
                styles.close()
        except OSError as e:
            print(e.strerror)
            print("No hay estilos!!!!")
        
        #componentes
        self.tabBar = QTabWidget(self)
        
        #configuraciones
        self.__config()
        
        #armado
        self.__build()
        
        #escuchas
        self.__listenings()
        
    #metodos de ventana
    def __config(self)->None:
        #configuracion de ventana
        self.setWindowTitle("Taskly - 0.0.1")
        self.setFixedSize(600, 400)
        self.setObjectName("main-window")
        
        #configuracion del tabBar
        self.tabBar.setFixedSize(self.size())
        self.tabBar.setFont(FNTELEMENT)
        
    def __build(self)->None:
        #adiciones al tab
        self.tabBar.addTab(TaskTab(self.tabBar), "Tareas")
        self.tabBar.addTab(ProjectTab(self.tabBar), "Proyectos")
    
    def __listenings(self)->None:
        pass
    
    def closeEvent(self, a0):
        #cierre de conexion a bd
        DBConector.closeConnection()
        #cierre formal
        super().closeEvent(a0)
        
        