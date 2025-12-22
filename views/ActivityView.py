from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QListWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QComboBox, QDateEdit)
from utils.constants import STATUS, PRIORITIES, FNTTEXTO, FNTTITLE, FNTELEMENT
from utils.observers import ProjectObserver
from .Dialogs import ActivityForm
from .Messages import info, warning, error
from models.taskModels import Activity
from utils.config import BASEDIR
from database.activities import ActivityApi
import os

class ActivityTab(QWidget):
    #constructor de clase
    def __init__(self, parent:QWidget, progress:ProjectObserver)->None:
        #instancia de padre
        super().__init__(parent)
        
        #hoja de estilos
        try:
            with open(os.path.join(BASEDIR,"assets","styles","task.css"),"r") as styles:
                self.setStyleSheet(styles.read())
                styles.close()
        except OSError as e:
            pass
        
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
        self.btnCreate.clicked.connect(self.createA)
        self.btnDelete.clicked.connect(self.deleteA)
        self.btnEdit.clicked.connect(self.editableA)
        self.btnSave.clicked.connect(self.saveA)
        self.btnComplete.clicked.connect(self.completeA)  
    
    def update(self)->None:
        #validar que no haya seleccion o que no sea el mismo proyecto
        if self.current and self.current.project == self.progress.id:
            return
        
        #limpiar items
        self.list.clear()
        
        #si se elimino, no agregar nada
        if self.progress.deleted:
            #eliminar de la base de datos
            for act in self.acts:
                #eliminar actividad
                self.api.deleteActivity(act.id)
            return
        
        #poner nuevos items
        self.acts = self.api.getActivities(self.progress.id)
        
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
            self.list.addItem(act.id)
            if act.status == 2:
                self.progress.adv += 1
            if act.status == 3:
                self.progress.end += 1
    
    #limpiar la seleccion
    def clearSelection(self)->None:
        #limpiar el current
        self.current = None
        
        #limpiar seleccion
        self.list.clearSelection()
        self.list.clearFocus()
        self.list.setCurrentRow(-1)
        
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
    def createA(self)->None:
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
            else:
                #mensaje de error
                error(self,"Actividad no creada","No se ha creado la actividad")
            del newAct
         
    def deleteA(self)->None:
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
            info(self, "Actividad eliminada","La actividad se ha eliminado")
        else:
            #mensaje de error
            error(self,"Actividad no eliminada","No se ha eliminado la actividad")
    
    def editableA(self)->None:
        #verificar seleccion
        if not self.current:
            #advertencia
            warning(self, "Sin seleccion", "Seleccione una actividad primero")
            return
        
        #activar la bandera
        self.editing = True
        
        #habilitar campos
        self.cbxPriority.setEnabled(True)
        if self.current.status != STATUS["terminada"]:
            self.cbxStatus.setEnabled(True)
        self.descText.setEnabled(True)
        
    def saveA(self)->None:
        #verificar seleccion
        if not self.current:
            #advertencia
            warning(self, "Sin seleccion", "Seleccione una actividad primero")
            return
        
        #desactivar la bandera
        self.editing = False
        
        #habilitar campos
        self.cbxPriority.setEnabled(False)
        self.cbxStatus.setEnabled(False)
        self.descText.setEnabled(False)
        
        #guardar el estatus previo
        prev_status = self.current.status
        
        #tomar los valores
        self.current.desc = self.descText.toPlainText()
        self.current.priority = PRIORITIES[self.cbxPriority.currentText()]
        self.current.status = STATUS[self.cbxStatus.currentText()]
        
        #mandar al api
        if self.api.updateActivity(self.current):
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
            info(self, "Actividad actualizada", "La actividad se ha actualizado")
        else:
            #mensaje de error
            error(self,"Actividad no creada","No se ha actualizado la actividad")
            
    def completeA(self)->None:
        #validar que exista una seleccion
        if not self.current:
            #advertencia
            warning(self, "Sin seleccion", "Seleccione una actividad primero")
            return
        
        #validar que no se este editando
        if self.editing:
            return
        
        #verificar el estatus
        if self.current.status == STATUS["terminada"]:
            warning(self, "Actividad completada", "La actividad ya esta completada")
            return
        
        if self.api.completeActivity(self.current.id):
            #actualizar el estatus
            self.current.status = STATUS["terminada"]
            #cambiar en el cbx
            self.cbxStatus.setCurrentIndex(STATUS["terminada"]-1)
            #actualizar en observer
            self.progress.end += 1
            self.progress.notify()
            #mensaje de exito
            info(self, "Actividad completada", "La actividad se marco como terminada")
        else:
            #mensaje de error
            error(self,"Actividad no completada","No se ha completado la actividad")