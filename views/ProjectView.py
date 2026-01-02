from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QListWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QComboBox, QDateEdit, QTableWidget, QTableWidgetItem)
from utils.constants import STATUS, FNTTEXTO, FNTTITLE, FNTELEMENT
from datetime import date
from .Dialogs import ProjectForm
from utils.config import BASEDIR
import os

class ProjectTab(QWidget):
    #constructor de clase
    def __init__(self)->None:
        #instancia de padre
        super().__init__()
        
        #hoja de estilos
        try:
            with open(os.path.join(BASEDIR,"assets","styles","tab.css"),"r") as styles:
                self.setStyleSheet(styles.read())
                styles.close()
        except OSError as e:
            pass
            
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
        
        #formulario de projectos
        self.projectForm = ProjectForm(self)
        
        #metodos de ventana
        self.__config()
        self.__build()
        
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
    
    #limpiar la seleccion
    def clearSelection(self)->None:
        #limpiar seleccion
        self.list.clearSelection()
        self.list.clearFocus()
        self.list.setCurrentRow(-1)
        
        #limpiar los campos
        self.fldName.setText('')
        self.date.setDate(date.today())
        self.cbxStatus.setCurrentIndex(0)
        self.descText.setText('')
        
        self.projectTable.setItem(0,0,QTableWidgetItem("0"))
        self.projectTable.setItem(0,1,QTableWidgetItem("0"))
        self.projectTable.setItem(0,2,QTableWidgetItem("0"))
        self.projectTable.setItem(0,3,QTableWidgetItem("0%"))