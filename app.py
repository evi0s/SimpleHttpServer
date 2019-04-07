"""Entry Point"""
import sys
import socket

import config
from utils.debug import *

# Add libs to sys path
sys.path.append(config.abspath)

if config.server_type == 'UNBLOCK':

    # Import Unblock socket server
    from unblockserver import server

elif config.server_type == 'ASYNC':

    # Import Async server
    from asyncserver import server

try:
    server()
except:
    error("An error has occurred!")
