from .schemas import task, simpletask
from .transactions import getKeys, getInfo, create, modify, drop
from models.taskModels import SimpleTask

class TaskApi:
    #metodos de operacion
    def getTaskIds(self)->list:
        return getKeys(simpletask)
    
    def getTask(self, id:str)->SimpleTask | None:
        tsk = getInfo(task,id)
        stsk = getInfo(simpletask,id)
        return SimpleTask(tsk["id"],stsk["title"],tsk["desc"],stsk["delivery"],tsk["priority"],tsk["status"]) if tsk and stsk else None
    
    def createTask(self, stsk:SimpleTask)->bool:
        dumped = stsk.asDict()
        i1 = create(task,dumped["tsk"])
        i2 = create(simpletask,dumped["stsk"])
        return True if i1 and i2 else False
    
    def deleteTask(self, id:str)->bool:
        return drop(task,id)
    
    def updateTask(self, stsk:SimpleTask)->bool:
        dumped = stsk.asDict()
        u1 = modify(task,dumped["tsk"])
        u2 = modify(simpletask,dumped["stsk"])
        return True if u1 and u2 else False
    
    def completeTask(self, id:str)->bool:
        return modify(task,{"id":id,"status": 3})