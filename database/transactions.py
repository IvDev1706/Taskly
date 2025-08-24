from .dbconnection import getSession
from sqlalchemy import select, insert, update, delete, Table, Selectable, Column
from sqlalchemy.exc import SQLAlchemyError

#metodos de transaccion
def getKeys(table:Table)->list:
    try:
        #obtener sesion
        db = getSession()
        #preparar el statement
        stmt = select(table.c["id"])
        #obtencion de los datos
        result = db.execute(stmt)
        data = result.fetchall()
        #retorno
        return [dict(id._mapping)["id"] for id in data]
    except SQLAlchemyError as e:
        return []
    
def getInfo(table:Table, id: str | int)->dict | None:
    try:
        #obtener la sesion
        db = getSession()
        #preparar el statement
        stmt = select(table).where(table.c["id"] == id)
        #obtencion de los datos
        result = db.execute(stmt)
        info = result.fetchone()
        #retorno de informacion
        return dict(info._mapping) if info else None
    except SQLAlchemyError as e:
        return None
    
def getJoin(table:Selectable, col:Column, value:str)->list:
    try:
        #obtener la sesion
        db = getSession()
        #preparar el statement
        stmt = select(table).where(col == value)
        #obtencion de los datos
        result = db.execute(stmt)
        data = result.fetchall()
        return [dict(row._mapping) for row in data]
    except SQLAlchemyError:
        return []

def create(table:Table, data:dict)->bool:
    try:
        #obtener la sesion
        db = getSession()
        #preparar la sentencia
        stmt = insert(table).values(data)
        #ejecutar la sentencia
        db.execute(stmt)
        db.commit()
        #mandar respuesta
        return True
    except SQLAlchemyError:
        return False
    
def modify(table:Table, data:dict)->bool:
    try:
        #obtener la sesion
        db = getSession()
        #preparar la sentencia
        stmt = update(table).where(table.c["id"] == data["id"]).values(data)
        #ejecutar la sentencia
        db.execute(stmt)
        db.commit()
        #mandar respuesta
        return True
    except SQLAlchemyError:
        return False
    
def drop(table:Table, id: str | int)->bool:
    try:
        #obtener la sesion
        db = getSession()
        #preparar la sentencia
        stmt = delete(table).where(table.c["id"] == id)
        #ejecutar la sentencia
        db.execute(stmt)
        db.commit()
        #mandar respuesta
        return True
    except SQLAlchemyError:
        return False