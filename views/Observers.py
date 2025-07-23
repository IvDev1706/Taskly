class ProjectObserver:
    #constructor de clase
    def __init__(self)->None:
        #atributos
        self.subjects = []
        
        #datos transitivos
        self.id = ""
        self.noActs = 0
        self.adv = 0
        self.end = 0
        
    def attachObservable(self, o)->None:
        self.subjects.append(o)
        
    def notify(self)->None:
        for subject in self.subjects:
            subject.update()