from PyQt6.QtWidgets import (QWidget, QTabWidget)
from PyQt6.QtGui import QIcon
from .TaskView import TaskTab
from .ProjectView import ProjectTab
from .ActivityView import ActivityTab
from .Observers import ProjectObserver
from .Messages import error
from utils.variables import FNTELEMENT
from utils.config import BASEDIR, VERSION
from database.dbconnection import closeSession
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
            pass
        
        #componentes
        self.tabBar = QTabWidget(self)
        self.taskTab = TaskTab(self.tabBar)
        #self.progress = ProjectObserver()
        #self.projectTab = ProjectTab(self.tabBar, self.progress)
        #self.activityTab = ActivityTab(self.tabBar, self.progress)
        #self.progress.attachObservable(self.activityTab)
        #self.progress.attachObservable(self.projectTab)
        
        #configuraciones
        self.__config()
        
        #armado
        self.__build()
        
        #escuchas
        self.__listenings()
        
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
        
    def __build(self)->None:
        #adiciones al tab
        self.tabBar.addTab(self.taskTab, "Tareas")
        #self.tabBar.addTab(self.projectTab, "Proyectos")
        #self.tabBar.addTab(self.activityTab, "Actividades")
    
    def __listenings(self)->None:
        self.tabBar.currentChanged.connect(self.onChange)
        
    def onChange(self, index:int)->None:
        #ver en que tab se cambio
        if index == 0:
            #limpiar seleccion en task
            self.taskTab.clearSelection()
        #elif index == 1:
            #limpiar seleccion en project
        #    self.projectTab.clearSelection()
        #else:
            #limpiar seleccion en activity
        #    self.activityTab.clearSelection()
    
    def closeEvent(self, a0):
        #cierre de sesion
        closeSession()
        #cierre formal
        super().closeEvent(a0)
        
        