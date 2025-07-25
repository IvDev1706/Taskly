from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QListWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QComboBox, QDateEdit, QTableWidget, QTableWidgetItem)
from utils.variables import STATUS, FNTTEXTO, FNTTITLE, FNTELEMENT
from .Messages import warning, info
from datetime import date
from .Dialogs import ProjectForm
from .Observers import ProjectObserver
from database.projectAPI import ProjectApi
from models.ProjectModels import Project

class ProjectTab(QWidget):
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
        self.lblName = QLabel(self)
        self.lblDelivery = QLabel(self)
        self.lblStatus = QLabel(self)
        self.btnCreate = QPushButton(self)
        self.btnDelete = QPushButton(self)
        self.btnEdit = QPushButton(self)
        self.btnSave = QPushButton(self)
        self.btnComplete = QPushButton(self)
        self.list = QListWidget(self)
        self.fldName = QLineEdit(self)
        self.date = QDateEdit(self)
        self.cbxStatus = QComboBox(self)
        self.descText = QTextEdit(self)
        self.projectTable = QTableWidget(1,4,self)
        
        #api de projectos
        self.api = ProjectApi()
        self.current = None
        self.projectForm = ProjectForm(self)
        
        #progreso de projecto
        self.progress = progress
        
        #banderas
        self.editing = False
        
        #metodos de ventana
        self.__config()
        self.__build()
        self.__listenings()
        
    def __config(self)->None:
        #configuracion de etiquetas
        self.lblName.setText("Project name")
        self.lblName.setFont(FNTTITLE)
        self.lblName.setObjectName("task-label")
        self.lblDelivery.setText("Project delivery")
        self.lblDelivery.setFont(FNTTITLE)
        self.lblDelivery.setObjectName("task-label")
        self.lblStatus.setText("Project status")
        self.lblStatus.setFont(FNTTITLE)
        self.lblStatus.setObjectName("task-label")
        
        #configuracion de campos
        self.list.addItems(self.api.getProjectIds())
        self.list.setFont(FNTELEMENT)
        self.list.setMaximumWidth(110)
        self.fldName.setFont(FNTELEMENT)
        self.fldName.setEnabled(False)
        self.date.setFont(FNTELEMENT)
        self.date.setDate(date.today())
        self.date.setEnabled(False)
        self.cbxStatus.setFont(FNTELEMENT)
        self.cbxStatus.addItems(STATUS.keys())
        self.cbxStatus.setEnabled(False)
        self.descText.setFont(FNTTEXTO)
        self.descText.setEnabled(False)
        #headers de la tabla
        self.projectTable.setObjectName("table")
        self.projectTable.setHorizontalHeaderLabels(["Num. activities","Advanced","Finished","% of complete"])
        self.projectTable.setMaximumHeight(80)
        self.projectTable.setItem(0,0,QTableWidgetItem("0"))
        self.projectTable.setItem(0,1,QTableWidgetItem("0"))
        self.projectTable.setItem(0,2,QTableWidgetItem("0"))
        self.projectTable.setItem(0,3,QTableWidgetItem("0%"))
        
        #configuracion de botones
        self.btnCreate.setText('+')
        self.btnCreate.setObjectName('task-button')
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
        infoG.addWidget(self.lblName,0,0)
        infoG.addWidget(self.fldName,1,0)
        infoG.addWidget(self.lblDelivery,0,1)
        infoG.addWidget(self.date,1,1)
        infoG.addWidget(self.lblStatus,0,2)
        infoG.addWidget(self.cbxStatus,1,2)
        infoG.addWidget(self.descText,2,0,2,3)
        infoG.addWidget(self.projectTable,5,0,1,3)
        mainH.addLayout(infoG)
        
        #ventana principal
        mainV = QVBoxLayout()
        mainV.addLayout(buttonsL)
        mainV.addLayout(mainH)
        
        #añadir a la ventana
        self.setLayout(mainV)
    
    def __listenings(self)->None:
        #esucuha de lista
        self.list.currentItemChanged.connect(self.setProject)
        
        #escuchas de botones
        self.btnCreate.clicked.connect(self.createP)
        self.btnDelete.clicked.connect(self.deleteP)
        self.btnEdit.clicked.connect(self.editableP)
        self.btnSave.clicked.connect(self.saveP)
        self.btnComplete.clicked.connect(self.completeP)
    
    #metodo de observer
    def update(self)->None:
        #poner las estadisticas
        self.projectTable.setItem(0,0,QTableWidgetItem(str(self.progress.noActs)))
        self.projectTable.setItem(0,1,QTableWidgetItem(str(self.progress.adv)))
        self.projectTable.setItem(0,2,QTableWidgetItem(str(self.progress.end)))
        self.projectTable.setItem(0,3,QTableWidgetItem("0%"))
        
    #limpiar la seleccion
    def clearSelection(self)->None:
        #limpiar el current
        self.current = None
        
        #limpiar los campos
        self.fldName.setText('')
        self.date.setDate(date.today())
        self.cbxStatus.setCurrentIndex(0)
        self.descText.setText('')
        
    def setProject(self)->None:
        #verificar que haya una señleccion
        item = self.list.currentItem()
        
        #si no hay cortar
        if not item:
            return
        
        #obtener la informacion
        self.current = self.api.getProject(item.data(0))
        
        if self.current:
            #guardar en progreso
            self.progress.id = self.current.id
            #colocar en los campos
            self.fldName.setText(self.current.name.strip())
            self.date.setDate(self.current.delivery)
            self.cbxStatus.setCurrentIndex(self.current.status-1)
            self.descText.setText(self.current.desc)
            self.progress.notify()
            
    def createP(self)->None:
        #validar que no se este editando
        if self.editing:
            return
        
        #abrir el modal
        if self.projectForm.exec():
            #datos capturados
            data = self.projectForm.data
            #paso a modelo y guardado en bd
            newProject = Project(*data, 1)
            if self.api.createProject(newProject):
                #añadir a la lista
                self.list.addItem(newProject.id)
                #mensaje de exito
                info(self,"Projecto creado","El projecto ha sido creado con exito")
            del newProject
        
    def deleteP(self)->None:
        #validar que haya una seleccion
        if not self.current:
            #advertencia
            warning(self, "Sin seleccion", "Seleccione un proyecto primero")
            return
        
        #validar que no se este editando
        if self.editing:
            return
        
        #eliminar del api
        if self.api.deleteProject(self.current.id):
            #remover de la lista
            self.list.takeItem(self.list.currentRow())
            self.list.setCurrentRow(-1)
            #limpiar los campos
            self.fldName.setText('')
            self.date.setDate(date.today())
            self.cbxStatus.setCurrentIndex(0)
            self.descText.setText('')
            #resetear el current
            self.current = None
            info(self, "Proyecto eliminado","El proyecto se ha eliminado")
    
    def editableP(self)->None:
        #validar que haya una seleccion
        if not self.current:
            #advertencia
            warning(self, "Sin seleccion", "Seleccione un proyecto primero")
            return
        
        self.editing = True
        #activar campos
        self.fldName.setEnabled(True)
        self.date.setEnabled(True)
        self.cbxStatus.setEnabled(True)
        self.descText.setEnabled(True)
        
    def saveP(self)->None:
        #validar que haya una seleccion
        if not self.current:
            #advertencia
            warning(self, "Sin seleccion", "Seleccione un proyecto primero")
            return
        
        self.editing = False
        #activar campos
        self.fldName.setEnabled(False)
        self.date.setEnabled(False)
        self.cbxStatus.setEnabled(False)
        self.descText.setEnabled(False)
        
        #tomar los valores
        self.current.name = self.fldName.text()
        self.current.desc = self.descText.toPlainText()
        self.current.delivery = date(self.date.date().year(), self.date.date().month(), self.date.date().day())
        self.current.status = STATUS[self.cbxStatus.currentText()]
        
        #mandar al api
        if self.api.updateProject(self.current):
                #mensaje de exito
                info(self, "Proyecto actualizado", "El proyecto se ha actualizado")
    
    def completeP(self)->None:
        #validar que exista una seleccion
        if not self.current:
            #advertencia
            warning(self, "Sin seleccion", "Seleccione un proyecto primero")
            return
        
        #validar que no se este editando
        if self.editing:
            return
        
        #verificar el estatus
        if self.current.status == STATUS["terminada"]:
            warning(self, "Proyecto completado", "El proyecto ya esta completado")
            return
        
        #actualizar el estatus
        self.current.status = STATUS["terminada"]
        #cambiar en el cbx
        self.cbxStatus.setCurrentIndex(STATUS["terminada"]-1)
        #mensaje de exito
        info(self, "Proyecto completado", "El proyecto se marco como terminado")