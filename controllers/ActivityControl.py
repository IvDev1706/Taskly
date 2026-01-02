from database import ActivityApi
from models import Activity
from views import ActivityTab
from views.Messages import info, error, warning
from utils.constants import STATUS, PRIORITIES
from utils.observers import ProjectObserver

class ActivityController:
    ### Metodo constructor ###
    def __init__(self, progress:ProjectObserver)->None:
        #objetos de vista y bd
        self.view = ActivityTab()
        self.dbapi = ActivityApi()
        
        #atributos
        self.current = None
        self.acts = []
        self.progress = progress
        self.editing = False
        
        #vincular escuchas
        self.__connect_listenings()

    ### Metodo de escuchas principal ###
    def __connect_listenings(self)->None:
        #escucha de lista
        self.view.list.currentItemChanged.connect(self.setActivity)
        
        #escuchas para botones
        self.view.btnCreate.clicked.connect(self.createA)
        self.view.btnDelete.clicked.connect(self.deleteA)
        self.view.btnEdit.clicked.connect(self.editableA)
        self.view.btnSave.clicked.connect(self.saveA)
        self.view.btnComplete.clicked.connect(self.completeA)
        
    ### Metodo de observer ###
    def update(self)->None:
        #validar que no haya seleccion o que no sea el mismo proyecto
        if self.current and self.current.project == self.progress.id:
            return
        
        #limpiar items
        self.view.list.clear()
        
        #si se elimino, no agregar nada
        if self.progress.deleted:
            #eliminar de la base de datos
            for act in self.acts:
                #eliminar actividad
                self.dbapi.deleteActivity(act.id)
            return
        
        #poner nuevos items
        self.acts = self.dbapi.getActivities(self.progress.id)
        
        #contar el numero de actividades
        self.progress.noActs = len(self.acts)
        
        #resetear las actividades
        self.progress.adv = 0
        self.progress.end = 0
        
        #si no tiene actividades
        if self.progress.noActs == 0:
            return
        
        #contar actividades avanzadas y finalizadas
        for act in self.acts:
            self.view.list.addItem(act.id)
            if act.status == 2:
                self.progress.adv += 1
            if act.status == 3:
                self.progress.end += 1
                
    ### Limpiar seleccion ###
    def clearSelection(self)->None:
        #limpiar el current
        self.current = None
        #limpiar seleccion
        self.view.clearSelection()
    
    ### Logica de escuchas ###
    #funcion de lista
    def setActivity(self)->None:
        #pide el item
        item = self.view.list.currentItem()

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
            self.view.fldTitle.setText(self.current.project)
            self.view.descText.setText(self.current.desc)
            self.view.cbxPriority.setCurrentIndex(self.current.priority-1)
            self.view.cbxStatus.setCurrentIndex(self.current.status-1)
    
    #funciones de botones
    def createA(self)->None:
        #verificar seleccion de proyecto
        if not self.progress.id:
            #advertencia
            warning(self.view, "Sin seleccion", "Seleccione un proyecto primero")
            return
        
        #verificar que no se este editando
        if self.editing:
            return
        
        #mostrar formulario
        if self.view.actForm.exec():
            #obtener datos
            data = self.view.actForm.data
            #pasar a modelo
            newAct = Activity(*data,1,self.progress.id)
            #mandar al api
            if self.dbapi.createActivity(newAct):
                #actualizar en observer
                self.progress.noActs += 1
                #añadir en caso de seleccion
                if self.current:
                   self.view.list.addItem(newAct.id)
                info(self.view, "Actividad creada", "La actividad ha sido creada")
                self.progress.notify()
            else:
                #mensaje de error
                error(self.view,"Actividad no creada","No se ha creado la actividad")
            del newAct
         
    def deleteA(self)->None:
        #validar que haya seleccion
        if not self.current:
            #advertencia
            warning(self.view, "Sin seleccion", "Seleccione una actividad primero")
            return
        
        #validar que no se este editando
        if self.editing:
            return
        
        #borrar en el api
        if self.dbapi.deleteActivity(self.current.id):
            #borrar de la lista
            self.view.list.takeItem(self.view.list.currentRow())
            self.view.list.setCurrentRow(-1)
            #limpiar campos
            self.view.fldTitle.setText('')
            self.view.cbxPriority.setCurrentIndex(0)
            self.view.cbxStatus.setCurrentIndex(0)
            self.view.descText.setText('')
            #actualiar en el observer
            self.progress.noActs -= 1
            self.progress.notify()
            #limpar el current
            self.current = None
            info(self.view, "Actividad eliminada","La actividad se ha eliminado")
        else:
            #mensaje de error
            error(self.view,"Actividad no eliminada","No se ha eliminado la actividad")
    
    def editableA(self)->None:
        #verificar seleccion
        if not self.current:
            #advertencia
            warning(self.view, "Sin seleccion", "Seleccione una actividad primero")
            return
        
        #activar la bandera
        self.editing = True
        
        #habilitar campos
        self.view.cbxPriority.setEnabled(True)
        if self.current.status != STATUS["terminada"]:
            self.view.cbxStatus.setEnabled(True)
        self.view.descText.setEnabled(True)
        
    def saveA(self)->None:
        #verificar seleccion
        if not self.current:
            #advertencia
            warning(self.view, "Sin seleccion", "Seleccione una actividad primero")
            return
        
        #desactivar la bandera
        self.editing = False
        
        #habilitar campos
        self.view.cbxPriority.setEnabled(False)
        self.view.cbxStatus.setEnabled(False)
        self.view.descText.setEnabled(False)
        
        #guardar el estatus previo
        prev_status = self.current.status
        
        #tomar los valores
        self.current.desc = self.view.descText.toPlainText()
        self.current.priority = PRIORITIES[self.view.cbxPriority.currentText()]
        self.current.status = STATUS[self.view.cbxStatus.currentText()]
        
        #mandar al api
        if self.dbapi.updateActivity(self.current):
            #actualizar en observer
            if prev_status == STATUS["no iniciada"] and self.current.status == STATUS["avanzada"]:
                self.progress.adv += 1
            if prev_status == STATUS["no iniciada"] and self.current.status == STATUS["terminada"]:
                self.progress.end += 1
            if prev_status == STATUS["avanzada"] and self.current.status == STATUS["no iniciada"]:
                self.progress.adv -= 1
            if prev_status == STATUS["avanzada"] and self.current.status == STATUS["terminada"]:
                self.progress.adv -= 1
                self.progress.end += 1
            self.progress.notify()
            #mensaje de exito
            info(self.view, "Actividad actualizada", "La actividad se ha actualizado")
        else:
            #mensaje de error
            error(self.view,"Actividad no creada","No se ha actualizado la actividad")
            
    def completeA(self)->None:
        #validar que exista una seleccion
        if not self.current:
            #advertencia
            warning(self.view, "Sin seleccion", "Seleccione una actividad primero")
            return
        
        #validar que no se este editando
        if self.editing:
            return
        
        #verificar el estatus
        if self.current.status == STATUS["terminada"]:
            warning(self.view, "Actividad completada", "La actividad ya esta completada")
            return
        
        if self.dbapi.completeActivity(self.current.id):
            #actualizar el estatus
            self.current.status = STATUS["terminada"]
            #cambiar en el cbx
            self.view.cbxStatus.setCurrentIndex(STATUS["terminada"]-1)
            #actualizar en observer
            self.progress.end += 1
            self.progress.notify()
            #mensaje de exito
            info(self.view, "Actividad completada", "La actividad se marco como terminada")
        else:
            #mensaje de error
            error(self.view,"Actividad no completada","No se ha completado la actividad")
