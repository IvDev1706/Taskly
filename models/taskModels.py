from datetime import date

class Task:
    # constructor
    def __init__(self, id: str, desc: str, priority: int, status: int)->None:
        #atributos
        self.id = id
        self.desc = desc
        self.priority = priority
        self.status = status
        
    def asRow(self)->list:
        return [self.id, self.desc,self.priority,self.status]
        
class SimpleTask(Task):
    #constructor
    def __init__(self, id: str, title: str, desc: str, delivery:date, priority: int, status: int)->None:
        #instancia de padre
        super().__init__(id, desc, priority, status)
        self.title = title
        self.delivery = delivery
        
    #sobreescritura
    def asRow(self)->list:
        return [super().asRow(),[self.id,self.title,self.delivery.strftime("%Y-%m-%d")]]

class Activity(Task):
    #constructor de clase
    def __init__(self, id:str, desc:str, priority:int, status:int, project:str)->None:
        #instancia de padre
        super().__init__(id, desc, priority, status)
        self.project = project
        
    def asRow(self)->list:
        return [super().asRow(),[self.id,self.project]]
    
    def __str__(self)->str:
        return self.id