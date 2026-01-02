from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QListWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QComboBox, QDateEdit)
from utils.constants import STATUS, PRIORITIES, FNTTEXTO, FNTTITLE, FNTELEMENT
from .Dialogs import ActivityForm
from utils.config import BASEDIR
import os

class ActivityTab(QWidget):
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
        
        #formulario de creacion
        self.actForm = ActivityForm(self)
        
        #metodos de ventana
        self.__config()
        self.__build()
        
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
    
    #limpiar la seleccion
    def clearSelection(self)->None:        
        #limpiar seleccion
        self.list.clearSelection()
        self.list.clearFocus()
        self.list.setCurrentRow(-1)
        
        #limpiar los campos
        self.fldTitle.setText('')
        self.cbxPriority.setCurrentIndex(0)
        self.cbxStatus.setCurrentIndex(0)
        self.descText.setText('')