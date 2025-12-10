from .metadata import PROJECTCOLUMNS, PROJECTTABLE
from .dbconnection import getInstance
from models.ProjectModels import Project
from utils.constants import STATUS
from datetime import datetime

class ProjectApi:
    #metodos del api
    def getProjectIds(self)->list:
        #obtener la conexion
        con = getInstance()
        #obtener los ids
        data = con.select_from(PROJECTTABLE,fields=[PROJECTCOLUMNS[0]])
        return [row[0] for row in data]
    
    def getProject(self, id:str)->Project:
        #obtener la conexion
        con = getInstance()
        #obtener informacion
        data = con.select_from(PROJECTTABLE,condition=PROJECTCOLUMNS[0]+"= '"+id+"'")[0]
        return Project(data[0],data[1],data[2],datetime.strptime(data[3],"%Y-%m-%d"),data[4])
    
    def createProject(self, prj:Project)->bool:
        #obtener la conexion
        con = getInstance()
        #volcar modelo
        data = prj.asRow()
        return con.insert_into(data,PROJECTTABLE)
    
    def deleteProject(self, id:str)->bool:
        #obtener la conexion
        con = getInstance()
        return con.delete_from(PROJECTTABLE,PROJECTCOLUMNS[0]+"= '"+id+"'")
    
    def updateProject(self, prj:Project)->bool:
        #obtener la conexion
        con = getInstance()
        #volcar modelo
        data = prj.asRow()
        return con.update_set(data,PROJECTCOLUMNS,PROJECTTABLE,PROJECTCOLUMNS[0]+"= '"+prj.id+"'")
    
    def completeProject(self, id:str)->bool:
        #obtener la conexion
        con = getInstance()
        return con.update_set([STATUS["terminada"]],[PROJECTCOLUMNS[4]],PROJECTTABLE,PROJECTCOLUMNS[0]+"= '"+id+"'")