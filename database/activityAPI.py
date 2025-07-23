from .dbconnection import DBConector
from models.taskModels import Activity
from psycopg2 import Error

class ActivityApi:
    #constructor de clase
    def __init__(self)->None:
        #instacia de conexion
        self.conn = DBConector.getConnection()
        
    #metodos de crud
    def getActivityIds(self, project: str)->list:
        #manejo de error
        try:
            #cursor de conexion
            cursor = self.conn.cursor()
            
            #sentencia
            cursor.execute(f'SELECT task_id FROM "FullActivity" WHERE activity_project = \'{project}\';')
            data = cursor.fetchall()
            
            #datos de regreso
            projects = []
            for row in data:
                projects.append(row[0])
            
            #cierre de tranasaccion
            cursor.close()
            self.conn.commit()
            
            #retorno de datos
            return projects
        except Error as e:
            print(f"Error({e.pgcode}): {e.pgerror}")
            return []
        
    def getActivity(self, id:str)->Activity:
        #manejo de error
        try:
            #cursor de conexion
            cursor = self.conn.cursor()
            
            #sentencia
            cursor.execute(f'SELECT * FROM "FullActivity" WHERE task_id = \'{id}\';')
            data = cursor.fetchall()
            
            #datos de regreso
            activity_data = data[0]
            activity = Activity(activity_data[0], activity_data[1], activity_data[4], activity_data[3], activity_data[2])
            
            #cierre de tranasaccion
            cursor.close()
            self.conn.commit()
            
            #retorno de datos
            return activity
        except Error as e:
            print(f"Error({e.pgcode}): {e.pgerror}")
            return None
        except IndexError as e:
            return None
    
    def createProject(self, activity:Activity)->bool:
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
            print(f"Error({e.pgcode}): {e.pgerror}")
            return False
        
    def updateProject(self, activity:Activity)->bool:
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
            print(f"Error({e.pgcode}): {e.pgerror}")
            return False
        
    def deleteProject(self, id:str)->bool:
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
            print(f"Error({e.pgcode}): {e.pgerror}")
            return False
        
    def completeProject(self, id:str)->bool:
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
            print(f"Error({e.pgcode}): {e.pgerror}")
            return False