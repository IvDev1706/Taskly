from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QListWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QComboBox, QDateEdit)
from utils.variables import STATUS, PRIORITIES, FNTTEXTO, FNTTITLE, FNTELEMENT
from .Observers import ProjectObserver
from .Dialogs import ActivityForm
from .Messages import info, warning
from models.taskModels import Activity
from database.activityAPI import ActivityApi

class ActivityTab(QWidget):
    #constructor de clase
    def __init__(self, parent:QWidget, progress:ProjectObserver)->None:
        #instancia de padre
        super().__init__(parent)
        
        #hoja de estilos
        try:
            with open("C:\\Users\\Ivan Cadena\\ProyectosPython\\Topicos\\Taskly\\assets\\styles\\task.css","r") as styles:
                self.setStyleSheet(styles.read())
                styles.close()
        except OSError as e:
            print(e.strerror)
            print("No hay estilos!!!!")
        
        #componentes
        self.list = QListWidget(self)
        self.btnCreate = QPushButton(self)
        self.btnDelete = QPushButton(self)
        self.btnEdit = QPushButton(self)
        self.btnSave = QPushButton(self)
        self.btnComplete = QPushButton(self)
        self.lblTitle = QLabel(self)
        self.lblPriority = QLabel(self)
        self.lblStatus = QLabel(self)
        self.fldTitle = QLineEdit(self)
        self.descText = QTextEdit(self)
        self.cbxStatus = QComboBox(self)
        self.cbxPriority = QComboBox(self)
        
        #api de base de datos
        self.api = ActivityApi()
        self.current = None
        self.acts = []
        self.progress = progress
        
        #banderas
        self.editing = False
        
        #formulario de creacion
        self.actForm = ActivityForm(self)
        
        #metodos de ventana
        self.__config()
        self.__build()
        self.__listenings()
        
    #metodos de ventana
    def __config(self)->None:
        #configuracion de componentes
        self.list.setFont(FNTELEMENT)
        self.list.setMaximumWidth(110)
        
        #etiquetas
        self.lblTitle.setText("Activity project")
        self.lblTitle.setObjectName("task-label")
        self.lblTitle.setFont(FNTTITLE)
        self.lblPriority.setText("Activity priority")
        self.lblPriority.setObjectName("task-label")
        self.lblPriority.setFont(FNTTITLE)
        self.lblStatus.setText("Activity status")
        self.lblStatus.setObjectName("task-label")
        self.lblStatus.setFont(FNTTITLE)
        
        #campos
        self.fldTitle.setFont(FNTELEMENT)
        self.fldTitle.setEnabled(False)
        self.cbxStatus.addItems(STATUS.keys())
        self.cbxStatus.setFont(FNTELEMENT)
        self.cbxStatus.setEnabled(False)
        self.cbxPriority.addItems(PRIORITIES.keys())
        self.cbxPriority.setFont(FNTELEMENT)
        self.cbxPriority.setEnabled(False)
        self.descText.setFont(FNTTEXTO)
        self.descText.setEnabled(False)
        
        #botones
        self.btnCreate.setText("+")
        self.btnCreate.setObjectName("task-button")
        self.btnCreate.setFont(FNTTEXTO)
        self.btnDelete.setText("-")
        self.btnDelete.setObjectName("task-button")
        self.btnDelete.setFont(FNTTEXTO)
        self.btnEdit.setText("edit")
        self.btnEdit.setObjectName("task-button")
        self.btnEdit.setFont(FNTTEXTO)
        self.btnSave.setText("save")
        self.btnSave.setObjectName("task-button")
        self.btnSave.setFont(FNTTEXTO)
        self.btnComplete.setText("complete")
        self.btnComplete.setObjectName("task-button")
        self.btnComplete.setFont(FNTTEXTO)
        
    def __build(self)->None:
        #panel de botones
        buttonsL = QHBoxLayout()
        buttonsL.addWidget(self.btnCreate)
        buttonsL.addWidget(self.btnDelete)
        buttonsL.addWidget(self.btnEdit)
        buttonsL.addWidget(self.btnSave)
        buttonsL.addWidget(self.btnComplete)
        
        #lista e informacion
        mainH = QHBoxLayout()
        mainH.addWidget(self.list)
        infoG = QGridLayout()
        infoG.addWidget(self.lblTitle,0,0)
        infoG.addWidget(self.fldTitle,1,0)
        infoG.addWidget(self.lblPriority,0,1)
        infoG.addWidget(self.cbxPriority,1,1)
        infoG.addWidget(self.lblStatus,0,2)
        infoG.addWidget(self.cbxStatus,1,2)
        infoG.addWidget(self.descText,2,0,1,3)
        mainH.addLayout(infoG)
        
        #ventana principal
        mainV = QVBoxLayout()
        mainV.addLayout(buttonsL)
        mainV.addLayout(mainH)
        
        #añadir a la ventana
        self.setLayout(mainV)
    
    def __listenings(self)->None:
        #escucha de lista
        self.list.currentItemChanged.connect(self.setActivity)
        
        #escuchas para botones
        self.btnCreate.clicked.connect(self.createT)
        self.btnDelete.clicked.connect(self.deleteT)
        self.btnEdit.clicked.connect(self.editableT)
        self.btnSave.clicked.connect(self.saveT)
        self.btnComplete.clicked.connect(self.completeT)  
    
    def update(self)->None:
        #validar que no haya seleccion o que no sea el mismo proyecto
        if self.current and self.current.project == self.progress.id:
            return
        
        #limpiar items
        self.list.clear()
        
        #poner nuevos items
        self.acts = self.api.getActivities(self.progress.id)
        
        #contar el numero de actividades
        self.progress.noActs = len(self.acts)
        
        #si no tiene actividades
        if self.progress.noActs == 0:
            return
        
        #contar actividades avanzadas y finalizadas
        for act in self.acts:
            self.list.addItem(act.id)
            if act.status == 2:
                self.progress.adv += 1
            if act.status == 3:
                self.progress.end += 1
    
    #limpiar la seleccion
    def clearSelection(self)->None:
        #limpiar el current
        self.current = None
        
        #limpiar los campos
        self.fldTitle.setText('')
        self.cbxPriority.setCurrentIndex(0)
        self.cbxStatus.setCurrentIndex(0)
        self.descText.setText('')
    
    #funcion de lista
    def setActivity(self)->None:
        #pide el item
        item = self.list.currentItem()

        #validar que exista
        if not item:
            return
        
        #obtener el id
        id = item.data(0)
        for act in self.acts:
            if act.id == id:
                self.current = act
                break
        
        #validar que se encontro
        if self.current:
            #actualizar campos
            self.fldTitle.setText(self.current.project)
            self.descText.setText(self.current.desc)
            self.cbxPriority.setCurrentIndex(self.current.priority-1)
            self.cbxStatus.setCurrentIndex(self.current.status-1)
    
    #funciones de botones
    def createT(self)->None:
        #verificar que no se este editando
        if self.editing:
            return
        
        #mostrar formulario
        if self.actForm.exec():
            #obtener datos
            data = self.actForm.data
            #pasar a modelo
            newAct = Activity(*data,1,self.progress.id)
            #mandar al api
            if self.api.createActivity(newAct):
                #actualizar en observer
                self.progress.noActs += 1
                #añadir en caso de seleccion
                if self.current:
                   self.list.addItem(newAct.id)
                info(self, "Actividad creada", "La actividad ha sido creada")
                self.progress.notify()
            del newAct
         
    def deleteT(self)->None:
        #validar que haya seleccion
        if not self.current:
            #advertencia
            warning(self, "Sin seleccion", "Seleccione una actividad primero")
            return
        
        #validar que no se este editando
        if self.editing:
            return
        
        #borrar en el api
        if self.api.deleteActivity(self.current.id):
            #borrar de la lista
            self.list.takeItem(self.list.currentRow())
            self.list.setCurrentRow(-1)
            #limpiar campos
            self.fldTitle.setText('')
            self.cbxPriority.setCurrentIndex(0)
            self.cbxStatus.setCurrentIndex(0)
            self.descText.setText('')
            #actualiar en el observer
            self.progress.noActs -= 1
            self.progress.notify()
            #limpar el current
            self.current = None
            info(self, "Actividad eliminado","La actividad se ha eliminado")
    
    def editableT(self)->None:
        pass
        
    def saveT(self)->None:
        pass
            
    def completeT(self)->None:
        pass