"""Config File"""
import os
import sys


abspath = os.getcwd()
defaultStaticDir = abspath + '/static'
defaultErrorDir = abspath + '/errorPage'
handlerPath = abspath + '/handler'

port = 80
if 'PORT' in os.environ:
    try:
        port = int(os.environ['PORT'])
    except ValueError as err:
        print(f"[Error]: {err}")
        sys.exit(0)
else:
    pass

host = os.environ['HOST'] if 'HOST' in os.environ else "0.0.0.0"
staticDir = os.environ['STATICDIR'] if 'STATICDIR' in os.environ else defaultStaticDir
errorDir = os.environ['ERRORDIR'] if 'ERRORDIR' in os.environ else defaultErrorDir
debug = True if 'DEBUG' in os.environ else False

server_type = 'UNBLOCK'

if 'SERVERTYPE' in os.environ:
    if os.environ['SERVERTYPE'] == 'ASYNC':
        server_type = 'ASYNC'
    elif os.environ['SERVERTYPE'] == 'MULTITHREAD':
        server_type = 'MULTITHREAD'
