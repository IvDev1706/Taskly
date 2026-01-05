class ProjectObserver:
    #constructor de clase
    def __init__(self)->None:
        #atributos
        self.subjects = []
        
        #datos transitivos
        self.id = ""
        self.deleted = False
        self.noActs = 0
        self.adv = 0
        self.end = 0
        
    def clearData(self)->None:
        self.id = ""
        self.deleted = False
        self.noActs = 0
        self.adv = 0
        self.end = 0
    
    ## metodos de observer ##
    def attachObservable(self, o)->None:
        self.subjects.append(o)
        
    def notify(self)->None:
        for subject in self.subjects:
            subject.update()
            
class CalendarObserver:
    #constructor de clase
    def __init__(self)->None:
        #atributos
        self.calendar = None
        self.subjects = []
        
        #ultimo modificado
        self.current = None
    
    ## metodos de observer ##
    def attachObservable(self, o)->None:
        self.subjects.append(o)
        
    def notify(self)->None:
        #notificar al calendario
        self.calendar.update()