from utils.config import SERVERCONFIG
import psycopg2 as pg

#clase conector
class DBConector:
    #variable de conexion
    __conn = None
    
    def getConnection():
        #validacion de instancia
        if not DBConector.__conn:
            #manejo de error
            try:
                DBConector.__conn = pg.connect(
                    dbname=SERVERCONFIG["bd"],
                    user=SERVERCONFIG["user"],
                    password=SERVERCONFIG["password"],
                    host=SERVERCONFIG["host"],
                    port=SERVERCONFIG["port"]
                )
                return DBConector.__conn
            except pg.Error as e:
                print(f"Error({e.pgcode}): {e.pgerror}")
                return DBConector.__conn
        else:
            return DBConector.__conn
        
    def closeConnection()->None:
        if DBConector.__conn:
            DBConector.__conn.close()