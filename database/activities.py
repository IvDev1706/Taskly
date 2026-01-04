from .metadata import TASKCOLUMNS, ACTIVITYTABLE, TASKTABLE, ACTIVITYCOLUMNS
from .dbconnection import getInstance
from models import Activity
from utils.constants import STATUS

class ActivityApi:
    #metodos de operacion
    def getActivities(self, prj:str)->list:
        #obtener conexion
        con = getInstance()
        #obtener actividades
        data = con.select_from("Full"+ACTIVITYTABLE,ACTIVITYCOLUMNS[1]+"= '"+prj+"'")
        return [Activity(row[0],row[1],row[2],row[3],row[4]) for row in data]
    
    def createActivity(self, act:Activity)->bool:
        #obtener conexion
        con = getInstance()
        #insertar los datos
        dumped = act.asRow()
        i1 = con.insert_into(dumped[0],TASKTABLE)
        i2 = con.insert_into(dumped[1],ACTIVITYTABLE)
        return True if i1 and i2 else False
    
    def deleteActivity(self, id:str)->bool:
        #obtener conexion
        con = getInstance()
        return con.delete_from(TASKTABLE,TASKCOLUMNS[0]+"= '"+id+"'")
    
    def updateActivity(self, act:Activity)->bool:
        #obtener conexion
        con = getInstance()
        #actualizar los datos
        dumped = act.asRow()
        return con.update_set(dumped[0],TASKCOLUMNS,TASKTABLE,TASKCOLUMNS[0]+"= '"+act.id+"'")
    
    def completeActivity(self, id:str)->bool:
        #obtener conexion
        con = getInstance()
        return con.update_set([STATUS["terminada"]],[TASKCOLUMNS[3]],TASKTABLE,TASKCOLUMNS[0]+"= '"+id+"'")