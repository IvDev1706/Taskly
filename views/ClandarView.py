from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QCalendarWidget, QLabel)
from PyQt6.QtCore import Qt
from utils.constants import FNTTITLE
from utils.config import BASEDIR
import os

class CalendarTab(QWidget):
    ### Metodo constructor ###
    def __init__(self)->None:
        #instancia de objeto padre
        super().__init__()
        
        #hoja de estilos
        try:
            with open(os.path.join(BASEDIR,"assets","styles","tab.css"),"r") as styles:
                self.setStyleSheet(styles.read())
                styles.close()
        except OSError as e:
            pass
        
        #componentes
        self.calendar = QCalendarWidget(self)
        self.lblCalendar = QLabel(self)
        
        #metodos de ventana
        self.__config()
        self.__build()
        
    ### Metodos de ventana ###
    def __config(self)->None:
        #etiquetas
        self.lblCalendar.setFont(FNTTITLE)
        self.lblCalendar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lblCalendar.setObjectName("tab-label")
        self.lblCalendar.setText("Pendings schedule")
        
        #componentes especiales
        self.calendar.setGridVisible(True)
        self.calendar.setSelectionMode(QCalendarWidget.SelectionMode.NoSelection)
        
    def __build(self)->None:
        #panel principal
        mainV = QVBoxLayout()
        
        #añadir elementos
        mainV.addWidget(self.lblCalendar)
        mainV.addWidget(self.calendar)
        
        #definir el layout
        self.setLayout(mainV)