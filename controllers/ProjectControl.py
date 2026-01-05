from PyQt6.QtWidgets import QTableWidgetItem
from database import ProjectApi
from models import Project
from views import ProjectTab
from views.Messages import info, error, warning
from utils.constants import STATUS
from utils.observers import ProjectObserver, CalendarObserver
from datetime import date

class ProjectController:
    ### Metodo constructor ###
    def __init__(self, progress:ProjectObserver, cal:CalendarObserver)->None:
        #objetos de vista y bd
        self.view = ProjectTab()
        self.dbapi = ProjectApi()
        
        #poner ids de proyectos
        self.view.list.addItems(self.dbapi.getProjectIds())
        
        #atributos
        self.editing = False
        self.current = None
        self.progress = progress
        self.cal = cal
        
        #vincular escuchas
        self.__connect_listenings()
        
    ### Metodo principal de escuchas ###
    def __connect_listenings(self)->None:
        #esucuha de lista
        self.view.list.currentItemChanged.connect(self.setProject)
        
        #escuchas de botones
        self.view.btnCreate.clicked.connect(self.createP)
        self.view.btnDelete.clicked.connect(self.deleteP)
        self.view.btnEdit.clicked.connect(self.editableP)
        self.view.btnSave.clicked.connect(self.saveP)
        self.view.btnComplete.clicked.connect(self.completeP)
    
    ### metodo de observer ###
    def update(self)->None:
        #si se elimino no hacer nada
        if self.progress.deleted:
            #limpiar la tabla
            self.view.projectTable.setItem(0,0,QTableWidgetItem("0"))
            self.view.projectTable.setItem(0,1,QTableWidgetItem("0"))
            self.view.projectTable.setItem(0,2,QTableWidgetItem("0"))
            self.view.projectTable.setItem(0,3,QTableWidgetItem("0%"))
            return
        #calcular porcentaje de trabajo
        work = 0 if self.progress.noActs == 0 else (self.progress.end/self.progress.noActs)*100
        #poner las estadisticas
        self.view.projectTable.setItem(0,0,QTableWidgetItem(str(self.progress.noActs)))
        self.view.projectTable.setItem(0,1,QTableWidgetItem(str(self.progress.adv)))
        self.view.projectTable.setItem(0,2,QTableWidgetItem(str(self.progress.end)))
        self.view.projectTable.setItem(0,3,QTableWidgetItem(f"{work}%"))
        
    ### limpiar la seleccion ###
    def clearSelection(self)->None:
        #limpiar el current
        self.current = None
        
        #limpiar seleccion
        self.view.clearSelection()
        
    ### logica de escuchas ###    
    def setProject(self)->None:
        #verificar que haya una señleccion
        item = self.view.list.currentItem()
        
        #si no hay cortar
        if not item:
            return
        
        #obtener la informacion
        self.current = self.dbapi.getProject(item.data(0))
        
        if self.current:
            #limpair datos del progreso
            self.progress.clearData()
            #guardar en progreso
            self.progress.id = self.current.id
            #colocar en los campos
            self.view.fldName.setText(self.current.name.strip())
            self.view.date.setDate(self.current.delivery)
            self.view.cbxStatus.setCurrentIndex(self.current.status-1)
            self.view.descText.setText(self.current.desc)
            self.progress.notify()
            
    def createP(self)->None:
        #validar que no se este editando
        if self.editing:
            return
        
        #abrir el modal
        if self.view.projectForm.exec():
            #datos capturados
            data = self.view.projectForm.data
            #paso a modelo y guardado en bd
            newProject = Project(*data, 1)
            if self.dbapi.createProject(newProject):
                #añadir a la lista
                self.view.list.addItem(newProject.id)
                #mensaje de exito
                info(self.view,"Projecto creado","El projecto ha sido creado con exito")
                #notificar al observer de calendario
                self.cal.current = newProject
                self.cal.notify()
            else:
                #mensaje de error
                error(self.view,"Proyecto no creado","No se ha creado el proyecto")
        
    def deleteP(self)->None:
        #validar que haya una seleccion
        if not self.current:
            #advertencia
            warning(self.view, "Sin seleccion", "Seleccione un proyecto primero")
            return
        
        #validar que no se este editando
        if self.editing:
            return
        
        #eliminar del api
        if self.dbapi.deleteProject(self.current.id):
            #remover de la lista
            self.view.list.takeItem(self.view.list.currentRow())
            self.view.list.setCurrentRow(-1)
            #limpiar los campos
            self.view.fldName.setText('')
            self.view.date.setDate(date.today())
            self.view.cbxStatus.setCurrentIndex(0)
            self.view.descText.setText('')
            self.view.projectTable.setItem(0,0,QTableWidgetItem("0"))
            self.view.projectTable.setItem(0,1,QTableWidgetItem("0"))
            self.view.projectTable.setItem(0,2,QTableWidgetItem("0"))
            self.view.projectTable.setItem(0,3,QTableWidgetItem("0%"))
            #resetear el current
            self.cal.current = self.current
            self.current = None
            info(self.view, "Proyecto eliminado","El proyecto se ha eliminado")
            #actualizar observer
            self.progress.deleted = True
            self.progress.notify()
            self.cal.notify()
        else:
            #mensaje de error
            error(self.view,"Proyecto no eliminado","No se ha eliminado el proyecto")
    
    def editableP(self)->None:
        #validar que haya una seleccion
        if not self.current:
            #advertencia
            warning(self.view, "Sin seleccion", "Seleccione un proyecto primero")
            return
        
        self.editing = True
        #activar campos
        self.view.fldName.setEnabled(True)
        self.view.date.setEnabled(True)
        if self.current.status != STATUS["terminada"]:
            self.view.cbxStatus.setEnabled(True)
        self.view.descText.setEnabled(True)
        
    def saveP(self)->None:
        #validar que haya una seleccion
        if not self.current:
            #advertencia
            warning(self.view, "Sin seleccion", "Seleccione un proyecto primero")
            return
        
        self.editing = False
        #activar campos
        self.view.fldName.setEnabled(False)
        self.view.date.setEnabled(False)
        self.view.cbxStatus.setEnabled(False)
        self.view.descText.setEnabled(False)
        
        #tomar los valores
        self.current.name = self.view.fldName.text()
        self.current.desc = self.view.descText.toPlainText()
        self.current.delivery = date(self.view.date.date().year(), self.view.date.date().month(), self.view.date.date().day())
        self.current.status = STATUS[self.view.cbxStatus.currentText()]
        
        #mandar al api
        if self.dbapi.updateProject(self.current):
                #mensaje de exito
                info(self.view, "Proyecto actualizado", "El proyecto se ha actualizado")
                #actualizar calendario
                self.cal.current = self.current
                self.cal.notify()
        else:
            #mensaje de error
            error(self.view,"Proyecto no actualizado","No se ha actualizado el proyecto")
    
    def completeP(self)->None:
        #validar que exista una seleccion
        if not self.current:
            #advertencia
            warning(self.view, "Sin seleccion", "Seleccione un proyecto primero")
            return
        
        #validar que no se este editando
        if self.editing:
            return
        
        #verificar el estatus
        if self.current.status == STATUS["terminada"]:
            warning(self.view, "Proyecto completado", "El proyecto ya esta completado")
            return
        
        #verificar el estatus
        if self.progress.end != self.progress.noActs:
            warning(self.view, "Proyecto incompleto", "No se han completado todas las actividades de este proyecto")
            return
        
        #mandar al api
        if self.dbapi.completeProject(self.current.id):
            #actualizar el estatus
            self.current.status = STATUS["terminada"]
            #cambiar en el cbx
            self.view.cbxStatus.setCurrentIndex(STATUS["terminada"]-1)
            #mensaje de exito
            info(self.view, "Proyecto completado", "El proyecto se marco como terminado")
            #actualizar observer
            self.cal.current = self.current
            self.cal.notify()
        else:
            #mensaje de error
            error(self.view,"Proyecto no completado","No se ha completado el proyecto")