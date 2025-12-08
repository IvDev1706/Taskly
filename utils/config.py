import json, os, sys


def get_base_dir():
    if getattr(sys, 'Frozen', False):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__name__))
#directorio base de forma dinamica
BASEDIR = get_base_dir()

#leer los datos de configuracion
with open(os.path.join(BASEDIR,'assets','config','cfg.json'),"r") as config:
    content = config.read()
    cfgdata = json.loads(content)
    config.close()
    
#configuracion de bd
DATABASE = os.path.join(BASEDIR, cfgdata["database"]["filename"])

#version de la aplicacion
VERSION = cfgdata['version']

#configuracion de fuentes
fnts = cfgdata['fonts']
FNTTEXTOCFG = fnts['text']
FNTTITLECFG = fnts['title']
FNTELEMENTCFG = fnts['elements']