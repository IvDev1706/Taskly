from .dbconnection import DBConector
from models.taskModels import Activity
from psycopg2 import Error

class ActivityApi:
    #constructor de clase
    def __init__(self)->None:
        #instacia de conexion
        self.conn = DBConector.getConnection()
        
    #metodos de crud
    def getActivities(self, project: str)->list:
        #manejo de error
        try:
            #cursor de conexion
            cursor = self.conn.cursor()
            
            #sentencia
            cursor.execute(f'SELECT * FROM "FullActivity" WHERE activity_project = \'{project}\';')
            data = cursor.fetchall()
            
            #datos de regreso
            projects = []
            for row in data:
                projects.append(Activity(row[0],row[1],row[4],row[3],row[2]))
            
            #cierre de tranasaccion
            cursor.close()
            self.conn.commit()
            
            #retorno de datos
            return projects
        except Error as e:
            #print(f"Error({e.pgcode}): {e.pgerror}")
            return []
    
    def createActivity(self, activity:Activity)->bool:
        #manejo de error
        try:
           #cursor de conexion
           cursor = self.conn.cursor()
           
           #sentencia
           sentencia = 'CALL createActivity(%s,%s,%s,%s,%s);'
           valores = activity.asTuple()
           cursor.execute(sentencia, valores)
           
           #cierre de transaccion
           cursor.close()
           self.conn.commit()
           
           #retorno de exito
           return True            
        except Error as e:
            #print(f"Error({e.pgcode}): {e.pgerror}")
            return False
        
    def updateActivity(self, activity:Activity)->bool:
        #manejo de error
        try:
           #cursor de conexion
           cursor = self.conn.cursor()
           
           #sentencia
           sentencia = 'CALL updateActivity(%s,%s,%s,%s,%s);'
           valores = activity.asTuple()
           cursor.execute(sentencia, valores)
           
           #cierre de transaccion
           cursor.close()
           self.conn.commit()
           
           #retorno de exito
           return True            
        except Error as e:
            #print(f"Error({e.pgcode}): {e.pgerror}")
            return False
        
    def deleteActivity(self, id:str)->bool:
        #manejo de error
        try:
            #cursor de conexion
            cursor = self.conn.cursor()
            
            #sentencia
            cursor.execute(f"CALL deleteActivity('{id}');")
            
            #cierre de transaccion
            cursor.close()
            self.conn.commit()
            
            #retorno de exito
            return True
        except Error as e:
            #print(f"Error({e.pgcode}): {e.pgerror}")
            return False
        
    def completeActivity(self, id:str)->bool:
        #manejo de error
        try:
            #cursor de conexion
            cursor = self.conn.cursor()
            
            #sentencia
            cursor.execute(f"CALL completeActivity('{id}');")
            
            #cierre de transaccion
            cursor.close()
            self.conn.commit()
            
            #retorno de exito
            return True
        except Error as e:
            #print(f"Error({e.pgcode}): {e.pgerror}")
            return False