from utils.config import SERVERCONFIG
import psycopg2 as pg

#clase conector
class DBConector:
    #variable de conexion
    conn = None
    
    def getConnection():
        #validacion de instancia
        if not DBConector.conn:
            #manejo de error
            try:
                DBConector.conn = pg.connect(
                    dbname=SERVERCONFIG["bd"],
                    user=SERVERCONFIG["user"],
                    password=SERVERCONFIG["password"],
                    host=SERVERCONFIG["host"],
                    port=SERVERCONFIG["port"]
                )
                return DBConector.conn
            except pg.Error as e:
                print(f"Error({e.pgcode}): {e.pgerror}")
                return DBConector.conn
        else:
            return DBConector.conn
        
    def closeConnection()->None:
        if DBConector.conn:
            DBConector.conn.close()