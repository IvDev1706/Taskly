from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QListWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QComboBox, QDateEdit)
from utils.variables import STATUS, PRIORITIES, FNTTEXTO, FNTTITLE, FNTELEMENT
from .Messages import warning, info
from datetime import date
from .Dialogs import TaskForm
from models.taskModels import SimpleTask
from database.taskAPI import TaskApi

class TaskTab(QWidget):
    #constructor de clase
    def __init__(self, parent:QWidget)->None:
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
        self.lblDelivery = QLabel(self)
        self.lblPriority = QLabel(self)
        self.lblStatus = QLabel(self)
        self.fldTitle = QLineEdit(self)
        self.descText = QTextEdit(self)
        self.cbxStatus = QComboBox(self)
        self.cbxPriority = QComboBox(self)
        self.date = QDateEdit(self)
        
        #api de base de datos
        self.api = TaskApi()
        self.current = None
        
        #banderas
        self.editing = False
        
        #formlario hijo
        self.taskForm = TaskForm(self)
        
        #metodos de ventana
        self.__config()
        self.__build()
        self.__listenings()
        
    #metodos de ventana
    def __config(self)->None:
        #configuracion de componentes
        self.list.setFont(FNTELEMENT)
        self.list.setMaximumWidth(110)
        self.list.addItems(self.api.getTaskIds())
        
        #etiquetas
        self.lblTitle.setText("Task title")
        self.lblTitle.setObjectName("task-label")
        self.lblTitle.setFont(FNTTITLE)
        self.lblDelivery.setText("Task delivery")
        self.lblDelivery.setFont(FNTTITLE)
        self.lblDelivery.setObjectName("task-label")
        self.lblPriority.setText("Task priority")
        self.lblPriority.setObjectName("task-label")
        self.lblPriority.setFont(FNTTITLE)
        self.lblStatus.setText("Task status")
        self.lblStatus.setObjectName("task-label")
        self.lblStatus.setFont(FNTTITLE)
        
        #campos
        self.fldTitle.setFont(FNTELEMENT)
        self.fldTitle.setEnabled(False)
        self.date.setFont(FNTELEMENT)
        self.date.setEnabled(False)
        self.date.setDate(date.today())
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
        infoG.addWidget(self.lblDelivery,0,1)
        infoG.addWidget(self.date,1,1)
        infoG.addWidget(self.lblPriority,0,2)
        infoG.addWidget(self.cbxPriority,1,2)
        infoG.addWidget(self.lblStatus,0,3)
        infoG.addWidget(self.cbxStatus,1,3)
        infoG.addWidget(self.descText,2,0,1,4)
        mainH.addLayout(infoG)
        
        #ventana principal
        mainV = QVBoxLayout()
        mainV.addLayout(buttonsL)
        mainV.addLayout(mainH)
        
        #añadir a la ventana
        self.setLayout(mainV)
    
    def __listenings(self)->None:
        #escucha de lista
        self.list.currentItemChanged.connect(self.setTask)
        
        #escuchas para botones
        self.btnCreate.clicked.connect(self.createT)
        self.btnDelete.clicked.connect(self.deleteT)
        self.btnEdit.clicked.connect(self.editableT)
        self.btnSave.clicked.connect(self.saveT)
        self.btnComplete.clicked.connect(self.completeT)  
    
    #funcion de lista
    def setTask(self)->None:
        #pide el item
        item = self.list.currentItem()

        #validar que exista
        if not item:
            return
        
        #obtener el id
        id = item.data(0)
        self.current = self.api.getTask(id)
        
        #actualizar campos
        self.fldTitle.setText(self.current.title.strip())
        self.descText.setText(self.current.desc)
        self.cbxPriority.setCurrentIndex(self.current.priority-1)
        self.cbxStatus.setCurrentIndex(self.current.status-1)
        self.date.setDate(self.current.delivery)
    
    #funciones de botones
    def createT(self)->None:
        #mientras se edita
        if self.editing:
            return
        
        #ejecutar el formulario y esperar a que se cierre
        if self.taskForm.exec():
            #datos capturados
            data = self.taskForm.data
            #paso a modelo y guardado en bd
            newTask = SimpleTask(*data,1)
            if self.api.createTask(newTask):
                #agregar a la lista
                self.list.addItem(newTask.id)
                #mensaje de exito
                info(self, "Tarea creada", "La tarea ha sido creada")
            del newTask
            
    def deleteT(self)->None:
        #mientras se edita
        if self.editing:
            return
        
        #validar si existe el current
        if self.current:
            #eliminar en el api
            if self.api.deleteTask(self.current.id):
                #eliminar de la lista
                self.list.takeItem(self.list.currentRow())
                self.list.setCurrentRow(-1)
                #limpiar los campos
                self.lblTitle.setText('Task title')
                self.date.setDate(date.today())
                self.cbxPriority.setCurrentIndex(0)
                self.cbxStatus.setCurrentIndex(0)
                self.descText.setText('')
                #quitar referencia
                self.current = None
                info(self, "Tarea eliminada","La tarea se ha eliminado")
        else:
            #advertencia
            warning(self, "Sin seleccion", "Seleccione una tarea primero")
    
    def editableT(self)->None:
        #validar si existe el current
        if self.current:
            self.editing = True
            #poner campos editables
            self.fldTitle.setEnabled(True)
            self.date.setEnabled(True)
            self.cbxPriority.setEnabled(True)
            self.cbxStatus.setEnabled(True)
            self.descText.setEnabled(True)
        else:
            #advertencia
            warning(self, "Sin seleccion", "Seleccione una tarea primero")
        
    def saveT(self)->None:
        #validar si existe el current
        if self.current:
            self.editing = False
            #quitar campos editables
            self.fldTitle.setEnabled(False)
            self.date.setEnabled(False)
            self.cbxPriority.setEnabled(False)
            self.cbxStatus.setEnabled(False)
            self.descText.setEnabled(False)
            
            #tomar los valores
            self.current.title = self.fldTitle.text()
            self.current.desc = self.descText.toPlainText()
            self.current.delivery = date(self.date.date().year(), self.date.date().month(), self.date.date().day())
            self.current.priority = PRIORITIES[self.cbxPriority.currentText()]
            self.current.status = STATUS[self.cbxStatus.currentText()]
            
            #mandar al api
            if self.api.updateTask(self.current):
                #mensaje de exito
                info(self, "Tarea actualizada", "La tarea se ha actualizado")
        else:
            #advertencia
            warning(self, "Sin seleccion", "Seleccione una tarea primero")
            
    def completeT(self)->None:
        #mientras se edita
        if self.editing:
            return
        
        #validar el current
        if self.current:
            #verificar el status
            if self.current.status != STATUS["terminada"]:
                self.current.status = STATUS["terminada"]
                #completar la tarea
                self.api.completeTask(self.current.id)
                #cambiar en el cbx
                self.cbxStatus.setCurrentIndex(STATUS["terminada"]-1)
                #mensaje de exito
                info(self, "Tarea completada", "La tarea se marco como terminada")
            else:
                warning(self, "Tarea completada", "La tarea ya esta completada")
        else:
            #advertencia
            warning(self, "Sin seleccion", "Seleccione una tarea primero")