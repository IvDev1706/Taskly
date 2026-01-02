from .TaskControl import TaskController
from .ProjectControl import ProjectController
from .ActivityControl import ActivityController
from views import MainWindow, CalendarTab
from utils.observers import ProjectObserver

class MasterController:
    ### Metodo constructor ###
    def __init__(self)->None:
        #objeto vista
        self.view = MainWindow()
        
        #observadores
        self.pobserver = ProjectObserver()
        
        #controladores
        self.tcontroller = TaskController()
        self.tcontroller.view.setParent(self.view)
        self.pcontroller = ProjectController(self.pobserver)
        self.pcontroller.view.setParent(self.view)
        self.acontroller = ActivityController(self.pobserver)
        self.acontroller.view.setParent(self.view)
        
        #añadir observadores
        self.pobserver.attachObservable(self.pcontroller)
        self.pobserver.attachObservable(self.acontroller)
        
        #añadir tabs
        self.view.tabBar.addTab(CalendarTab(),"Agenda")
        self.view.tabBar.addTab(self.tcontroller.view,"Tareas")
        self.view.tabBar.addTab(self.pcontroller.view,"Proyectos")
        self.view.tabBar.addTab(self.acontroller.view,"Actividades")
        
        #vincular escuchas
        self.__connect_listenings()
    
    ### Metodo principal de escuchas ###
    def __connect_listenings(self)->None:
        #escucha de lista
        self.view.tabBar.currentChanged.connect(self.onChange)
        
    #limpiar el foco de seleccion al cambiar de pestaña
    def onChange(self, index:int)->None:
        #limpiar seleccion en todos los tabs
        self.tcontroller.clearSelection()
        self.pcontroller.clearSelection()
        self.acontroller.clearSelection()
        
    def display(self)->None:
        #desplegar ventana
        self.view.show()
    