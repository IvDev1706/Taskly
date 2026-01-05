from .metadata import SIMPLETASKCOLUMNS, SIMPLETASKTABLE, PROJECTCOLUMNS, PROJECTTABLE
from .dbconnection import getInstance
from models import Project, SimpleTask
from datetime import datetime


class CalendarApi:
    #metodos de operacion
    def getTasksByDate(self, month:int, year:int)->list:
        #obtener instancia
        con = getInstance()
        
        #preparar condicion
        cond = SIMPLETASKCOLUMNS[2]+f" like '{year}-{month}-__'" if month > 10 else SIMPLETASKCOLUMNS[2]+f" like '{year}-0{month}-__'"
        
        #obtener tareas
        data = con.select_from("full"+SIMPLETASKTABLE,cond)
        
        #retornar tareas
        return [SimpleTask(row[0],row[1],row[2],datetime.strptime(row[3],"%Y-%m-%d"),row[4],row[5]) for row in data]
    
    def getProjectsByDate(self, month:int, year:int)->list:
        #obtener instancia
        con = getInstance()
        
        #preparar condicion
        cond = PROJECTCOLUMNS[3]+f" like '{year}-{month}-__'" if month > 10 else PROJECTCOLUMNS[3]+f" like '{year}-0{month}-__'"
        
        #obtener tareas
        data = con.select_from(PROJECTTABLE,cond)
        
        #retornar tareas
        return [Project(row[0],row[1],row[2],datetime.strptime(row[3],"%Y-%m-%d"),row[4]) for row in data]