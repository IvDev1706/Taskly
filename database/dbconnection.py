from utils.config import DATABASE
import sqlite3

class DBConnector:
    #insiancia unica
    driver = None
    #metodo constructor
    def __init__(self)->None:
        #atributos
        self.con = sqlite3.connect(DATABASE)
        cursor = self.con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        self.con.commit()
        
    #metodos de instancia
    def close_connection(self)->None:
        #cerrar la conexion si existe
        if self.con: 
            self.con.close()
    
    def select_from(self, table:str, condition:str = "", fields:list = ["*"])->list:
        try:
            #obtener cursor de conexion
            cursor = self.con.cursor()
            
            #preparar el statement
            stmt = "SELECT "+", ".join(fields) if len(fields) != 1 else "SELECT "+fields[0]
            stmt += " FROM "+table
            stmt += " WHERE "+condition+";" if condition != "" else ";"
            
            #ejecutar la sentencia y obtener datos
            res = cursor.execute(stmt)
            
            return res.fetchall()
        except sqlite3.Error as e:
            return []
        
    def insert_into(self, values:list, table:str, fields:list = None)->bool:
        try:
            #obtener cursor de conexion
            cursor = self.con.cursor()
            
            #preparar el statement
            stmt = "INSERT INTO "+table+"("+", ".join(fields)+")" if fields else "INSERT INTO "+table
            stmt += " VALUES ("+", ".join(["?" for val in values])+");"
            
            #ejecutar el statement 
            cursor.execute(stmt,tuple(values))
            
            #cierre de transaccion
            self.con.commit()
            
            #retornar verdadero
            return True
        except sqlite3.Error as e:
            #retornar falso
            return False
        
    def update_set(self, values:list, fields:list, table:str, condition:str)->bool:
        try:
            #obtener cursor de conexion
            cursor = self.con.cursor()
            
            #preparar el statement
            stmt = "UPDATE "+table+" SET "+"= ?, ".join(fields)+"= ? WHERE "+condition+";"
            
            #ejecutar el statement
            cursor.execute(stmt, tuple(values))
            
            #cierre de transaccion
            self.con.commit()
            
            #retornar verdadero
            return True
        except sqlite3.Error as e:
            #retornar falso
            return False
        
    def delete_from(self, table:str, condition:str)->bool:
        try:
            #obtener cursor de conexion
            cursor = self.con.cursor()
            
            #preparar el statement
            stmt = "DELETE FROM "+table+" WHERE "+condition+";"
            
            #ejecutar el statement
            cursor.execute(stmt)
            
            #cierre de transaccion
            self.con.commit()
            
            #retornar verdadero
            return True
        except sqlite3.Error as e:
            #retornar falso
            return False
        
#metodo de singleton
def getInstance()->DBConnector:
    #validar instancia
    if DBConnector.driver:
        return DBConnector.driver
    return DBConnector()