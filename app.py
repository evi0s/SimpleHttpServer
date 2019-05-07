"""Entry Point"""
import sys
import socket

import config
from utils.debug import *

# Add libs to sys path
sys.path.append(config.abspath)
sys.path.append(config.handlerPath)

if config.server_type == 'UNBLOCK':

    # Import Unblock socket server
    from unblockserver import server

elif config.server_type == 'ASYNC':

    # Import Async server
    from asyncserver import server

else:

    # Import Multi Thread server
    from multithreadserver import server

try:
    server()
except Exception as e:
    error("An error has occurred!")
    error(e.args)
