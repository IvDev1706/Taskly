from .schemas import project
from .transactions import getKeys, getInfo, create, drop, modify
from models.ProjectModels import Project

class ProjectApi:
    #metodos del api
    def getProjectIds(self)->list:
        return getKeys(project)
    
    def getProject(self, id:str)->Project | None:
        dict = getInfo(project,id)
        return Project(**dict)
    
    def createProject(self, prj:Project)->bool:
        return create(project,prj.asDict())
    
    def deleteProject(self, id:str)->bool:
        return drop(project,id)
    
    def updateProject(self, prj:Project)->bool:
        return modify(project,prj.asDict())