"""Entry Point"""
import sys
import socket

import config
from utils.debug import *
from handler.handler import *

# Add libs to sys path
sys.path.append(config.abspath)
# Setup server socket
debug("Setting up server socket...")
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind Host and Port
try:
    serverSocket.bind((config.host, config.port))
    debug("Listening on host: %s, port: %s" % (config.host, config.port))
except OSError as err:
    error(err.args[1])
    sys.exit(0)

# Connection pool
serverSocket.listen(150)

# Non-blocking
serverSocket.setblocking(False)
debug("Server socket setup finished.")

clientConnections = []

# Infinite loop
while True:

    try:
        connectionSocket, clientAddress = serverSocket.accept()
        debug("Client: " + connectionSocket.__str__())
        clientConnections.append(connectionSocket)
    except BlockingIOError:
        # Block IO

        # Dead connections
        deadConnections = []

        # Handle connections
        for connectionSocket in clientConnections:
            try:
                # Receive request
                clientRequest = connectionSocket.recv(1024)
                debug("Request: " + str(clientRequest))

                # Handle request
                clientResponse = handle(clientRequest)
                debug("Response: " + str(clientResponse))

                # Send Response
                connectionSocket.send(clientResponse)

                # Close connection
                connectionSocket.close()
                clientConnections.remove(connectionSocket)
            except BlockingIOError:
                continue

            # Connection reset
            except ConnectionResetError:
                connectionSocket.close()
                deadConnections.append(connectionSocket)

            # Keyboard interrupt
            except KeyboardInterrupt:
                error("KeyboardInterrupt")
                sys.exit(0)

        # Clean dead connections
        for connectionSocket in deadConnections:
            clientConnections.remove(connectionSocket)

    except KeyboardInterrupt:
        error("KeyboardInterrupt")
        sys.exit(0)
