from database.dbconnection import DBConector
from models.ProjectModels import Project
import psycopg2 as pg

class ProjectApi:
    #constructor de clase
    def __init__(self)->None:
        #instacia de conexion
        self.conn = DBConector.getConnection()
        
    #metodos de crud
    def getProjectIds(self)->list:
        #manejo de error
        try:
            #cursor de conexion
            cursor = self.conn.cursor()
            
            #sentencia
            cursor.execute('SELECT project_id FROM "Project";')
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
        except pg.Error as e:
            #print(f"Error({e.pgcode}): {e.pgerror}")
            return []
        
    def getProject(self, id:str)->Project:
        #manejo de error
        try:
            #cursor de conexion
            cursor = self.conn.cursor()
            
            #sentencia
            cursor.execute(f'SELECT * FROM "Project" WHERE project_id = \'{id}\';')
            data = cursor.fetchall()
            
            #datos de regreso
            project_data = data[0]
            project = Project(*project_data)
            
            #cierre de tranasaccion
            cursor.close()
            self.conn.commit()
            
            #retorno de datos
            return project
        except pg.Error as e:
            #print(f"Error({e.pgcode}): {e.pgerror}")
            return None
        except IndexError as e:
            return None
    
    def createProject(self, project:Project)->bool:
        #manejo de error
        try:
           #cursor de conexion
           cursor = self.conn.cursor()
           
           #sentencia
           sentencia = 'CALL createProject(%s,%s,%s,%s,%s);'
           valores = project.asTuple()
           cursor.execute(sentencia, valores)
           
           #cierre de transaccion
           cursor.close()
           self.conn.commit()
           
           #retorno de exito
           return True            
        except pg.Error as e:
            #print(f"Error({e.pgcode}): {e.pgerror}")
            return False
        
    def updateProject(self, project:Project)->bool:
        #manejo de error
        try:
           #cursor de conexion
           cursor = self.conn.cursor()
           
           #sentencia
           sentencia = 'CALL updateProject(%s,%s,%s,%s,%s);'
           valores = project.asTuple()
           cursor.execute(sentencia, valores)
           
           #cierre de transaccion
           cursor.close()
           self.conn.commit()
           
           #retorno de exito
           return True            
        except pg.Error as e:
            #print(f"Error({e.pgcode}): {e.pgerror}")
            return False
        
    def deleteProject(self, id:str)->bool:
        #manejo de error
        try:
            #cursor de conexion
            cursor = self.conn.cursor()
            
            #sentencia
            cursor.execute(f"CALL deleteProject('{id}');")
            
            #cierre de transaccion
            cursor.close()
            self.conn.commit()
            
            #retorno de exito
            return True
        except pg.Error as e:
            #print(f"Error({e.pgcode}): {e.pgerror}")
            return False
        
    def completeProject(self, id:str)->bool:
        #manejo de error
        try:
            #cursor de conexion
            cursor = self.conn.cursor()
            
            #sentencia
            cursor.execute(f"CALL completeProject('{id}');")
            
            #cierre de transaccion
            cursor.close()
            self.conn.commit()
            
            #retorno de exito
            return True
        except pg.Error as e:
            #print(f"Error({e.pgcode}): {e.pgerror}")
            return False