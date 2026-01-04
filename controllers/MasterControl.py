from .TaskControl import TaskController
from .ProjectControl import ProjectController
from .ActivityControl import ActivityController
from .CalendarControl import CalendarController
from views import MainWindow
from utils.observers import ProjectObserver

class MasterController:
    ### Metodo constructor ###
    def __init__(self)->None:
        #objeto vista
        self.view = MainWindow()
        
        #observadores
        self.pobserver = ProjectObserver()
        
        #controladores
        self.ccontroller = CalendarController()
        self.ccontroller.view.setParent(self.view)
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
        self.view.tabBar.addTab(self.ccontroller.view,"Schedule")
        self.view.tabBar.addTab(self.tcontroller.view,"Tasks")
        self.view.tabBar.addTab(self.pcontroller.view,"Projects")
        self.view.tabBar.addTab(self.acontroller.view,"Activities")
        
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
    