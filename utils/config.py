import json, os

#directorio base de forma dinamica
BASEDIR = os.path.dirname(os.path.abspath(__name__))

#leer los datos de configuracion
with open(BASEDIR+"\\assets\\config\\cfg.json","r") as config:
    content = config.read()
    cfgdata = json.loads(content)
    config.close()
    
#configuracion de bd
SERVERCONFIG = cfgdata['database']

#configuracion de fuentes
fnts = cfgdata['fonts']
FNTTEXTOCFG = fnts['text']
FNTTITLECFG = fnts['title']
FNTELEMENTCFG = fnts['elements']