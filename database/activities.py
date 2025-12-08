from models.taskModels import Activity

class ActivityApi:
    #metodos de operacion
    def getActivities(self, prj:str)->list:
        data = getJoin(activity.join(task, activity.c["id"] == task.c["id"]),activity.c["project"],prj)
        return [Activity(row["id"],row["desc"],row["priority"],row["status"],row["project"]) for row in data]
    
    def createActivity(self, act:Activity)->bool:
        dumped = act.asDict()
        i1 = create(task,dumped["tsk"])
        i2 = create(activity,dumped["act"])
        return True if i1 and i2 else False
    
    def deleteActivity(self, id:str)->bool:
        return drop(task,id)
    
    def updateActivity(self, act:Activity)->bool:
        dumped = act.asDict()
        u1 = modify(task,dumped["tsk"])
        u2 = modify(activity,dumped["act"])
        return True if u1 and u2 else False
    
    def completeActivity(self, id:str)->bool:
        return modify(task,{"id":id,"status": 3})