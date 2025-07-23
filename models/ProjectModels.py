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
    def asTuple(self)->tuple:
        return (self.id, self.name, self.desc, self.delivery, self.status)