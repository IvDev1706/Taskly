from .metadata import TASKCOLUMNS, SIMPLETASKTABLE, TASKTABLE, SIMPLETASKCOLUMNS
from .dbconnection import getInstance
from models.taskModels import SimpleTask
from utils.constants import STATUS
from datetime import datetime

class TaskApi:
    #metodos de operacion
    def getTaskIds(self)->list:
        #obtener conexion
        con = getInstance()
        data = con.select_from(SIMPLETASKTABLE,fields=[TASKCOLUMNS[0]])
        return [row[0] for row in data]
    
    def getTask(self, id:str)->SimpleTask | None:
        #obtener conexion
        con = getInstance()
        data = con.select_from("Full"+SIMPLETASKTABLE,condition=TASKCOLUMNS[0]+"='"+id+"'")[0]
        return SimpleTask(data[0],data[1],data[2],datetime.strptime(data[3],"%Y-%m-%d"),data[4],data[5])
    
    def createTask(self, stsk:SimpleTask)->bool:
        #obtener conexion
        con = getInstance()
        #dumpear el modelo
        dumped = stsk.asRow()
        i1 = con.insert_into(dumped[0],TASKTABLE)
        i2 = con.insert_into(dumped[1],SIMPLETASKTABLE)
        return True if i1 and i2 else False
    
    def deleteTask(self, id:str)->bool:
        #obtener conexion
        con = getInstance()
        return con.delete_from(TASKTABLE,TASKCOLUMNS[0]+"= '"+id+"'")
    
    def updateTask(self, stsk:SimpleTask)->bool:
        #obtener conexion
        con = getInstance()
        #dumpear el modelo
        dumped = stsk.asRow()
        u1 = con.update_set(dumped[0],TASKCOLUMNS,TASKTABLE,TASKCOLUMNS[0]+"= '"+stsk.id+"'")
        u2 = con.update_set(dumped[1],SIMPLETASKCOLUMNS,SIMPLETASKTABLE,TASKCOLUMNS[0]+"= '"+stsk.id+"'")
        return True if u1 and u2 else False
    
    def completeTask(self, id:str)->bool:
        #obtener conexion
        con = getInstance()
        return con.update_set([STATUS["terminada"]],[TASKCOLUMNS[3]],TASKTABLE,TASKCOLUMNS[0]+"= '"+id+"'")