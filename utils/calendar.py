from PyQt6.QtCore import QDate
from PyQt6.QtGui import QColor
from .constants import OVERDUEDAY, PENDINGDAY, ADVANCEDDAY, COMPLETEDDAY, STATUS, REVERSESTATUS
from datetime import datetime
from models import SimpleTask, Project

class ClassifiedDay:
    ### Metodo constructor ###
    def __init__(self)->None:
        #atributos
        self.date = None
        self.tooltip = ""
        self.color = None
    

class DayClassifier:
    ### Metodo constructor ###
    def __init__(self, tasks:list, projects:list)->None:
        #atributos
        self.days = {}
        self.classified = []
        
        #clasificar los dias
        self.__group(tasks,projects)
        self.__classify()
        
    #clasificacion de dias
    def __group(self, tasks:list, projects:list)->None:
        date = ""
        #agrupar tareas por dia
        for tsk in tasks:
            date = tsk.delivery.strftime("%Y-%m-%d")
            #verificar si ya esta en la lista
            if not date in self.days.keys():
                self.days[date] = [tsk]
            else:
                self.days[date].append(tsk)
                
        #agrupar proyectos por dia
        for prj in projects:
            date = prj.delivery.strftime("%Y-%m-%d")
            #verificar si ya esta en la lista
            if not date in self.days.keys():
                self.days[date] = [prj]
            else:
                self.days[date].append(prj)
                
    def __classify(self)->None:
        #contenedores
        cday = None
        stats = {STATUS["no iniciada"]:0,STATUS["avanzada"]:0,STATUS["terminada"]:0}
        tooltips = []
        
        #iterar los dias
        for day in self.days.values():
            #objeto dia
            cday = ClassifiedDay()
            cday.date = QDate(day[0].delivery.year,day[0].delivery.month,day[0].delivery.day)
            #iterar pendientes del dia
            for p in day:
                #contar estatus
                stats[p.status] += 1
                #añadir al tooltip
                try:
                    tooltips.append(f"{p.id} - {p.title} ({REVERSESTATUS[p.status-1]})")
                except AttributeError as e:
                    tooltips.append(f"{p.id} - {p.name} ({REVERSESTATUS[p.status-1]})")
            #definir tooltips
            cday.tooltip = self.__getTooltip(tooltips)
            #mapear color
            cday.color = self.__mapColor(stats, day[0].delivery)
            #añadir el dia
            self.classified.append(cday)
            #reiniciar estats
            stats[STATUS["no iniciada"]] = 0
            stats[STATUS["avanzada"]] = 0
            stats[STATUS["terminada"]] = 0
            #reiniciar tooltip
            tooltips = []
            
    def __mapColor(self, stats:dict, date:datetime)->QColor: 
        #caso 1 - todo completo
        if not stats[STATUS["avanzada"]] and not stats[STATUS["no iniciada"]]:
            #color verde
            return COMPLETEDDAY
        #caso 2 - vencido o retrazado
        elif date < datetime.today():
            return OVERDUEDAY
        #caso 3 - todo en no iniciado
        if not stats[STATUS["avanzada"]] and not stats[STATUS["terminada"]]:
            #color gris
            return PENDINGDAY
        #caso 4 - todo disparejo
        else:
            return ADVANCEDDAY

    def __getTooltip(self,tooltips)->str:
        tooltip = ""
        #si es menor a 4 regresar el tooltip
        if len(tooltips) < 5:
            for i in range(len(tooltips)):
                #añadir al tooltip
                tooltip += tooltips[i]+"\n"
            return tooltip[:-1]
        else:
            for i in range(4):
                #añadir al tooltip
                tooltip += tooltips[i]+"\n"
            return tooltip + "..."