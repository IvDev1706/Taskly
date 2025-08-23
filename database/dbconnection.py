from utils.config import SERVERCONFIG
from utils.variables import STATUS, PRIORITIES
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker
from .schemas import metadata, status, prioprities

#motor de base de datos
engine = create_engine(SERVERCONFIG["dialect"])

#crear la seson
SesionLocal = sessionmaker(autoflush=False, bind=engine)

#sesion unica
singlesession = None

def start_db():
    #motor global de bd
    global engine
    #crear las tablas
    metadata.create_all(engine)
    #prinsertar las prioridades y estatus
    db = getSession()
    stmt = insert(status).prefix_with("OR IGNORE").values([{"name":sts} for sts in STATUS.keys()])
    db.execute(stmt)
    stmt = insert(status).prefix_with("OR IGNORE").values([{"name":pri} for pri in PRIORITIES.keys()])
    db.execute(stmt)
    db.commit()

def getSession():
    global singlesession
    if not singlesession:
        singlesession = SesionLocal()
        return singlesession
    else:
        return singlesession

def closeSession():
    if singlesession:
        singlesession.close()