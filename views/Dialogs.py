from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QDateEdit, QPushButton, QLabel, QTextEdit)
from PyQt6.QtCore import Qt
from utils.variables import FNTTEXTO, FNTTITLE, FNTELEMENT, STATUS, PRIORITIES
from datetime import date

class BaseForm(QDialog):
    #constructor
    def __init__(self, parent):
        #instancia de padre
        super().__init__(parent)
        
        #configuracion
        self.setFixedSize(300,400)
        self.setModal(True)
        self.setObjectName("form-cont")
        
        #componentes
        self.mainV = QVBoxLayout()
        self.formL = QFormLayout()
        self.btnGuardar = QPushButton(self)
        self.btnGuardar.setText("guardar")
        self.btnGuardar.setObjectName("task-button")
        self.btnGuardar.clicked.connect(self.__save)
        self.setLayout(self.mainV)

    #metodos a sobreescribir
    def __save(self)->None:
        self.close()
    
    def __clean(self)->None:
        pass
    
class TaskForm(BaseForm):
    #constructor
    def __init__(self, parent)->None:
        #instancia de padre
        super().__init__(parent)
        
        #config
        super().setWindowTitle("New Task")
        
        #componentes
        self.lblTitle = QLabel(self)
        self.lblId = QLabel(self)
        self.fldId = QLineEdit(self)
        self.lblTaskTitle = QLabel(self)
        self.fldTitle = QLineEdit(self)
        self.lblDelivery = QLabel(self)
        self.fldDelivery = QDateEdit(self)
        self.lblPriority = QLabel(self)
        self.cbxPriority = QComboBox(self)
        self.lblDesc = QLabel(self)
        self.descText = QTextEdit(self)
        
        #configuracion
        self.__config()
        
        #armado del formulario
        self.__build()
        
    def __config(self)->None:
        self.lblTitle.setFont(FNTTITLE)
        self.lblTitle.setText("Nueva tarea")
        self.lblTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lblTitle.setObjectName("task-label")
        self.lblId.setFont(FNTTEXTO)
        self.lblId.setText("ID (3 chars.):")
        self.lblId.setObjectName("task-label")
        self.lblTaskTitle.setFont(FNTTEXTO)
        self.lblTaskTitle.setText("Ttitulo:")
        self.lblTaskTitle.setObjectName("task-label")
        self.lblDelivery.setFont(FNTTEXTO)
        self.lblDelivery.setText("fecha de entrega:")
        self.lblDelivery.setObjectName("task-label")
        self.lblPriority.setFont(FNTTEXTO)
        self.lblPriority.setText("Nivel de eprioridad:")
        self.lblPriority.setObjectName("task-label")
        self.lblDesc.setFont(FNTTEXTO)
        self.lblDesc.setText("Descripcion:")
        self.lblDesc.setObjectName("task-label")
        self.fldId.setPlaceholderText("XXX")
        self.fldTitle.setPlaceholderText("Algun titulo")
        self.fldDelivery.setDate(date.today())
        self.cbxPriority.addItems(PRIORITIES.keys())
        self.descText.setPlaceholderText("Alguna descripcion")
        
    def __build(self)->None:
        self.mainV.addWidget(self.lblTitle)
        self.formL.addRow(self.lblId,self.fldId)
        self.formL.addRow(self.lblTaskTitle, self.fldTitle)
        self.formL.addRow(self.lblDelivery, self.fldDelivery)
        self.formL.addRow(self.lblPriority, self.cbxPriority)
        self.mainV.addLayout(self.formL)
        self.mainV.addWidget(self.lblDesc)
        self.mainV.addWidget(self.descText)
        self.mainV.addWidget(self.btnGuardar)