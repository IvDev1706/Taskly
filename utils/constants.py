from PyQt6.QtGui import QFont, QColor
from .config import FNTTITLECFG, FNTTEXTOCFG, FNTELEMENTCFG

#fuentes
FNTTITLE = QFont(FNTTITLECFG[0],FNTTITLECFG[1])
FNTTEXTO = QFont(FNTTEXTOCFG[0],FNTTEXTOCFG[1])
FNTELEMENT = QFont(FNTELEMENTCFG[0],FNTELEMENTCFG[1])
FNTTITLE.setBold(True)

#lista de prioridades
PRIORITIES = {
    "no importa": 1,
    "ligera": 2,
    "regular": 3,
    "relevante": 4,
    "urgente": 5
}

#lista de status
STATUS = {
    "no iniciada": 1,
    "avanzada": 2,
    "terminada": 3,
}

#mapeo inverso
REVERSESTATUS = ["no iniciada","avanzada","terminada"]

#meses del año
MONTHS = [
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre"
]

#colores de calendario
OVERDUEDAY = QColor("#ff3322")
PENDINGDAY = QColor("#555555")
ADVANCEDDAY = QColor("#3355ff")
COMPLETEDDAY = QColor("#33ff55")