from datetime import date

class Task:
    # constructor
    def __init__(self, id: str, desc: str, priority: int, status: int)->None:
        #atributos
        self.id = id
        self.desc = desc
        self.priority = priority
        self.status = status
        
    def asDict(self)->dict:
        return {"id":self.id, "desc":self.desc, "priority":self.priority, "status":self.status}
        
class SimpleTask(Task):
    #constructor
    def __init__(self, id: str, title: str, desc: str, delivery:date, priority: int, status: int)->None:
        #instancia de padre
        super().__init__(id, desc, priority, status)
        self.title = title
        self.delivery = delivery
        
    #sobreescritura
    def asDict(self)->dict:
        return {"tsk":super().asDict(),"stsk":{"id":self.id,"title":self.title.strip(), "delivery":self.delivery}}

class Activity(Task):
    #constructor de clase
    def __init__(self, id:str, desc:str, priority:int, status:int, project:str)->None:
        #instancia de padre
        super().__init__(id, desc, priority, status)
        self.project = project
        
    def asDict(self)->dict:
        return {"tsk":super().asDict(),"act":{"id":self.id,"project":self.project}}
    
    def __str__(self)->str:
        return self.id