from datetime import date

class Task:
    # constructor
    def __init__(self, id: str, desc: str, priority: int, status: int)->None:
        #atributos
        self.id = id
        self.desc = desc
        self.priority = priority
        self.status = status
        
    def asTuple(self)->tuple:
        return (self.id, self.desc, self.priority, self.status)
        
class SimpleTask(Task):
    #constructor
    def __init__(self, id: str, title: str, desc: str, delivery:date, priority: int, status: int)->None:
        #instancia de padre
        super().__init__(id, desc, priority, status)
        self.title = title
        self.delivery = delivery
        
    #sobreescritura
    def asTuple(self)->tuple:
        return (self.id, self.title.strip(), self.desc, self.delivery.strftime("%d/%m/%Y"), self.priority, self.status)

class Activity(Task):
    #constructor de clase
    def __init__(self, id:str, desc:str, priority:int, status:int, project:str)->None:
        #instancia de padre
        super().__init__(id, desc, priority, status)
        self.project = project
        
    def asTuple(self)->tuple:
        return (self.id, self.desc, self.priority, self.status, self.project)
    
    def __str__(self)->str:
        return self.id