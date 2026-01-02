from views import TaskTab
from views.Messages import info, warning, error
from database import TaskApi
from models import SimpleTask
from datetime import date
from utils.constants import STATUS, PRIORITIES

class TaskController:
    ### metodo constructor ###
    def __init__(self)->None:
        #objetos de vista y de base de datos
        self.dbapi = TaskApi()
        self.view = TaskTab()
        
        #poner ids de tareas
        self.view.list.addItems(self.dbapi.getTaskIds())
        
        #atributos
        self.current = None
        self.editing = False
        
        #vincular escuchas
        self.__connect_listenings()
        
    ### metodo principal de escucha ###
    def __connect_listenings(self)->None:
        #escucha de lista
        self.view.list.currentItemChanged.connect(self.setTask)
        
        #escuchas para botones
        self.view.btnCreate.clicked.connect(self.createT)
        self.view.btnDelete.clicked.connect(self.deleteT)
        self.view.btnEdit.clicked.connect(self.editableT)
        self.view.btnSave.clicked.connect(self.saveT)
        self.view.btnComplete.clicked.connect(self.completeT)
        
    ### logica de escuchas ###
    
    #funcion de lista
    def setTask(self)->None:
        #pide el item
        item = self.view.list.currentItem()

        #validar que exista
        if not item:
            return
        
        #obtener el id
        id = item.data(0)
        self.current = self.dbapi.getTask(id)
        
        #actualizar campos
        self.view.fldTitle.setText(self.current.title.strip())
        self.view.descText.setText(self.current.desc)
        self.view.cbxPriority.setCurrentIndex(self.current.priority-1)
        self.view.cbxStatus.setCurrentIndex(self.current.status-1)
        self.view.date.setDate(self.current.delivery)
    
    #funciones de botones
    def createT(self)->None:
        #mientras se edita
        if self.editing:
            return
        
        #ejecutar el formulario y esperar a que se cierre
        if self.view.taskForm.exec():
            #datos capturados
            data = self.view.taskForm.data
            #paso a modelo y guardado en bd
            newTask = SimpleTask(*data,1)
            if self.dbapi.createTask(newTask):
                #agregar a la lista
                self.view.list.addItem(newTask.id)
                #mensaje de exito
                info(self.view, "Tarea creada", "La tarea ha sido creada")
            del newTask
        else:
            #mensaje de error
            error(self.view,"Tarea no creada","No se ha creado la tarea")
            
    def deleteT(self)->None:
        #validar si existe el current
        if not self.current:
            #advertencia
            warning(self.view, "Sin seleccion", "Seleccione una tarea primero")
            return
        
        #mientras se edita
        if self.editing:
            return
        
        #eliminar en el api
        if self.dbapi.deleteTask(self.current.id):
            #eliminar de la lista
            self.view.list.takeItem(self.view.list.currentRow())
            self.view.list.setCurrentRow(-1)
            #limpiar los campos
            self.view.fldTitle.setText('')
            self.view.date.setDate(date.today())
            self.view.cbxPriority.setCurrentIndex(0)
            self.view.cbxStatus.setCurrentIndex(0)
            self.view.descText.setText('')
            #quitar referencia
            self.current = None
            info(self.view, "Tarea eliminada","La tarea se ha eliminado")
        else:
            #mensaje de error
            error(self.view,"Tarea no eliminada","No se ha creado la tarea")
            
    
    def editableT(self)->None:
        #validar si existe el current
        if not self.current:
            #advertencia
            warning(self.view, "Sin seleccion", "Seleccione una tarea primero")
            return
        
        #encender bandera
        self.editing = True
        
        #poner campos editables
        self.view.fldTitle.setEnabled(True)
        self.view.date.setEnabled(True)
        self.view.cbxPriority.setEnabled(True)
        if self.current.status != STATUS["terminada"]:
            self.view.cbxStatus.setEnabled(True)
        self.view.descText.setEnabled(True)
        
    def saveT(self)->None:
        #validar si existe el current
        if not self.current:
            #advertencia
            warning(self.view, "Sin seleccion", "Seleccione una tarea primero")
            return
        
        #encender bandera
        self.editing = False
        
        #quitar campos editables
        self.view.fldTitle.setEnabled(False)
        self.view.date.setEnabled(False)
        self.view.cbxPriority.setEnabled(False)
        self.view.cbxStatus.setEnabled(False)
        self.view.descText.setEnabled(False)
        
        #tomar los valores
        self.current.title = self.view.fldTitle.text()
        self.current.desc = self.view.descText.toPlainText()
        self.current.delivery = date(self.view.date.date().year(), self.view.date.date().month(), self.view.date.date().day())
        self.current.priority = PRIORITIES[self.view.cbxPriority.currentText()]
        self.current.status = STATUS[self.view.cbxStatus.currentText()]
        
        #mandar al api
        if self.dbapi.updateTask(self.current):
            #mensaje de exito
            info(self.view, "Tarea actualizada", "La tarea se ha actualizado")
        else:
            #mensaje de error
            error(self.view,"Tarea no actualizada","No se ha actualizado la tarea")
            
    def completeT(self)->None:
        #validar seleccion
        if not self.current:
            #advertencia
            warning(self.view, "Sin seleccion", "Seleccione una tarea primero")
            return
        
        #mientras se edita
        if self.editing:
            return
        
        #verificar el status
        if self.current.status == STATUS["terminada"]:
            warning(self.view, "Tarea completada", "La tarea ya esta completada")
            return
        
        #marcar como terminado
        self.current.status = STATUS["terminada"]
        #completar la tarea
        if self.dbapi.completeTask(self.current.id):
            #cambiar en el cbx
            self.view.cbxStatus.setCurrentIndex(STATUS["terminada"]-1)
            #mensaje de exito
            info(self.view, "Tarea completada", "La tarea se marco como terminada")
        else:
            #mensaje de error
            error(self.view,"Tarea no completada","No se ha completado la tarea")
            
    def clearSelection(self)->None:
        #limpiar el current
        self.current = None
        #limpiar ventana
        self.view.clearSelection()
    