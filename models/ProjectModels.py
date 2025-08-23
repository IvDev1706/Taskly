from datetime import date

class Project:
    #constructor
    def __init__(self, id:str, name:str, desc:str, delivery:date, status:int)->None:
        #atributos
        self.id = id
        self.name = name
        self.desc = desc
        self.delivery = delivery
        self.status = status
        
    #paso a tupla
    def asDict(self)->tuple:
        return {"id":self.id, "name":self.name, "desc":self.desc, "delivery":self.delivery, "status":self.status}