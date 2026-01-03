from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QCalendarWidget, QLabel, QPushButton, QComboBox, QSpinBox)
from PyQt6.QtCore import Qt
from utils.constants import FNTTITLE, FNTTEXTO, FNTELEMENT
from utils.config import BASEDIR
from datetime import date
import os

class CalendarTab(QWidget):
    ### Metodo constructor ###
    def __init__(self)->None:
        #instancia de objeto padre
        super().__init__()
        
        #hoja de estilos
        try:
            with open(os.path.join(BASEDIR,"assets","styles","calendar.css"),"r") as styles:
                self.setStyleSheet(styles.read())
                styles.close()
        except OSError as e:
            pass
        
        #componentes
        self.calendar = QCalendarWidget(self)
        self.lblCalendar = QLabel(self)
        self.btnNext = QPushButton(self)
        self.btnPrev = QPushButton(self)
        self.month = QComboBox(self)
        self.year = QSpinBox(self)
        
        #metodos de ventana
        self.__config()
        self.__build()
        
    ### Metodos de ventana ###
    def __config(self)->None:
        #etiquetas
        self.lblCalendar.setFont(FNTTITLE)
        self.lblCalendar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lblCalendar.setObjectName("calendar-label")
        self.lblCalendar.setText("Pendings schedule")
        
        #botones
        self.btnNext.setFont(FNTTEXTO)
        self.btnNext.setObjectName("calendar-button")
        self.btnNext.setText(">")
        self.btnPrev.setFont(FNTTEXTO)
        self.btnPrev.setObjectName("calendar-button")
        self.btnPrev.setText("<")
        
        #campos
        dt = date.today()
        self.month.addItems(["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"])
        self.month.setFont(FNTELEMENT)
        self.month.setObjectName("calendar-combo")
        self.month.setCurrentIndex(dt.month-1)
        self.year.setFont(FNTELEMENT)
        self.year.setObjectName("calendar-spin")
        self.year.setMaximum(9999)
        self.year.setValue(dt.year)
        
        #componentes especiales
        self.calendar.setGridVisible(True)
        self.calendar.setObjectName("calendar")
        self.calendar.setNavigationBarVisible(False)
        self.calendar.setSelectionMode(QCalendarWidget.SelectionMode.NoSelection)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.calendar.setHorizontalHeaderFormat(QCalendarWidget.HorizontalHeaderFormat.NoHorizontalHeader)
        
    def __build(self)->None:
        #panel principal
        mainV = QVBoxLayout()
        
        #panel de botones
        lHorizontal = QHBoxLayout()
        lHorizontal.addWidget(self.btnPrev)
        lHorizontal.addWidget(self.month)
        lHorizontal.addWidget(self.year)
        lHorizontal.addWidget(self.btnNext)
        
        #añadir elementos
        mainV.addWidget(self.lblCalendar)
        mainV.addLayout(lHorizontal)
        mainV.addWidget(self.calendar)
        
        #definir el layout
        self.setLayout(mainV)