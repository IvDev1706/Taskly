import json

#leer los datos de configuracion
with open("C:\\Users\\Ivan Cadena\\ProyectosPython\\Topicos\\Taskly\\assets\\config\\cfg.json","r") as config:
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