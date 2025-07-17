from database.dbconnection import DBConector
from models.taskModels import SimpleTask
import psycopg2 as pg

class TaskApi:
    #construtor de clase
    def __init__(self):
        #atributos
        self.conn = DBConector.getConnection()
    
    #metodos de crud
    def getTaskIds(self)->list:
        #manejo de error
        try:
            #cursor de conexion
            cursor = self.conn.cursor()
            
            #ejecucion de sentencia
            cursor.execute('SELECT task_id FROM "FullTask";')
            data = cursor.fetchall()
            
            #paso a modelo
            tasks = []
            for row in data:
                tasks.append(row[0])
            
            #cierre de transaccion
            cursor.close()
            self.conn.commit()
            
            #retorno de lista
            return tasks
        except pg.Error as e:
            print(f"Error({e.pgcode}): {e.pgerror}")
            return []
        
    def getTask(self, id:str)->SimpleTask:
        #manejo de error
        try:
            #cursor de conexion
            cursor = self.conn.cursor()
            
            #ejecucion de sentencia
            cursor.execute(f'SELECT * FROM "FullTask" WHERE task_id = \'{id}\';')
            data = cursor.fetchall()
            
            #paso a modelo
            task = SimpleTask(data[0][0],data[0][1],data[0][3],data[0][2],data[0][5],data[0][4])
            
            #cierre de transaccion
            cursor.close()
            self.conn.commit()
            
            #retorno de lista
            return task
        except pg.Error as e:
            print(f"Error({e.pgcode}): {e.pgerror}")
            return None
        except IndexError as e:
            print(f"Error: {e}")
            return None
    
    def createTask(self, task:SimpleTask)->bool:
        #manejo de error
        try:
            #cursor de conexion
            cursor = self.conn.cursor()
            
            #ejecucion de sentencia
            values = task.asTuple()
            cursor.execute('CALL createSimpleTask(%s,%s,%s,%s,%s,%s);',values)
            
            #cierre de transaccion
            cursor.close()
            self.conn.commit()
            
            #retorno de exito
            return True
        except pg.Error as e:
            print(f"Error({e.pgcode}): {e.pgerror}")
            return False
        
    def updateTask(self, task:SimpleTask)->bool:
        #manejo de error
        try:
            #cursor de conexion
            cursor = self.conn.cursor()
            
            #ejecucion de sentencia
            values = task.asTuple()
            cursor.execute('CALL updateSimpleTask(%s,%s,%s,%s,%s,%s);',values)
            
            #cierre de transaccion
            cursor.close()
            self.conn.commit()
            
            #retorno de exito
            return True
        except pg.Error as e:
            print(f"Error({e.pgcode}): {e.pgerror}")
            return False
        
    def deleteTask(self, id:str)->bool:
        #manejo de error
        try:
            #cursor de conexion
            cursor = self.conn.cursor()
            
            #ejecucion de sentencia
            cursor.execute(f"CALL deleteSimpleTask('{id}');")
            
            #cierre de transaccion
            cursor.close()
            self.conn.commit()
            
            #retorno de exito
            return True
        except pg.Error as e:
            print(f"Error({e.pgcode}): {e.pgerror}")
            return False
        
    def completeTask(self, id:str)->bool:
        #manejo de error
        try:
            #cursor de conexion
            cursor = self.conn.cursor()
            
            #ejecucion de sentencia
            cursor.execute(f"CALL completeTask('{id}');")
            
            #cierre de transaccion
            cursor.close()
            self.conn.commit()
            
            #retorno de exito
            return True
        except pg.Error as e:
            print(f"Error({e.pgcode}): {e.pgerror}")
            return False