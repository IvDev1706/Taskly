
from PyQt6.QtGui import QTextCharFormat, QColor
from views import CalendarTab
from database import CalendarApi
from utils.calendar import DayClassifier

class CalendarController:
    ### Metodo constructor ###
    def __init__(self)->None:
        #objetos de vista y bd
        self.view = CalendarTab()
        self.dbapi = CalendarApi()
        
        #atributos
        self.current_month = self.view.month.currentIndex() + 1
        self.current_year = self.view.year.value()
        
        #poner fechas en el calendario
        self.clf = DayClassifier(self.dbapi.getTasksByDate(self.current_month, self.current_year),self.dbapi.getProjectsByDate(self.current_month, self.current_year))
        self.__display_dates()
        
        #metodo de escuchas principal
        self.__connect_listenings()
        
    ### Metodo para desplegar fechas ###
    def __display_dates(self)->None:
        #contenedores
        fmt = None
        
        #iterar en dias
        for day in self.clf.classified:
            #instanciar un nuevo formato
            fmt = QTextCharFormat()
            fmt.setForeground(QColor("#ffffff"))
            fmt.setBackground(day.color)
            fmt.setToolTip(day.tooltip)
            
            #añadir al calendario
            self.view.calendar.setDateTextFormat(day.date,fmt)
        
        
    ### Metodo principal de escuchas ###
    def __connect_listenings(self)->None:
        #escuchas de boton previo
        self.view.btnPrev.clicked.connect(self.set_prev)
        self.view.btnNext.clicked.connect(self.set_next)
        
        #escuchas de selectores
        self.view.month.currentIndexChanged.connect(self.set_month)
        self.view.year.valueChanged.connect(self.set_year)
        
    ### Logica de escuchas ###
    def set_prev(self)->None:
        #verificar si es enero de cualquier año
        if self.current_month == 1:
            #restar 1 al año actual
            self.current_year -= 1
            #fijar a diciembre del año
            self.current_month = 12
        else:
            #restar 1 al mes
            self.current_month -= 1
            
        #actualizar campos
        self.view.month.setCurrentIndex(self.current_month-1)
        self.view.year.setValue(self.current_year)
        self.view.calendar.setCurrentPage(self.current_year, self.current_month)
    
    def set_next(self)->None:
        #verificar si es diciembre de cualquier año
        if self.current_month == 12:
            #sumar 1 al año actual
            self.current_year += 1
            #fijar a enero del año
            self.current_month = 1
        else:
            #sumar 1 al mes
            self.current_month += 1
            
        #actualizar campos
        self.view.month.setCurrentIndex(self.current_month-1)
        self.view.year.setValue(self.current_year)
        self.view.calendar.setCurrentPage(self.current_year, self.current_month)
        
    def set_month(self)->None:
        #obtener el mes
        self.current_month = self.view.month.currentIndex() + 1
        
        #actualizar el calendario
        self.view.calendar.setCurrentPage(self.current_year, self.current_month)
        
    def set_year(self)->None:
        #obtener el mes
        self.current_year = self.view.year.value()
        
        #actualizar el calendario
        self.view.calendar.setCurrentPage(self.current_year, self.current_month)
        