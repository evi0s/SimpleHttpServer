import sys
import socket

import config
from utils.debug import *
from handler.handler import *


def server():
    # Setup server socket
    debug("Setting up server socket...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind Host and Port
    try:
        server_socket.bind((config.host, config.port))
        debug("Listening on host: %s, port: %s" % (config.host, config.port))
    except OSError as err:
        error(err.args[1])
        sys.exit(0)

    # Connection pool
    server_socket.listen(150)

    # Non-blocking
    server_socket.setblocking(False)
    debug("Server socket setup finished.")

    client_connections = []

    # Infinite loop
    while True:

        try:
            connection_socket, client_address = server_socket.accept()
            debug("Client: " + connection_socket.__str__())
            client_connections.append(connection_socket)
        except BlockingIOError:
            # Block IO

            # Dead connections
            dead_connections = []

            # Handle connections
            for connection_socket in client_connections:
                try:
                    # Receive request
                    client_request = connection_socket.recv(1024)
                    debug("Request: " + str(client_request))

                    # Handle request
                    client_request = str(client_request, encoding='utf-8')
                    client_response = handle(client_request)
                    debug("Response: " + str(client_response))

                    # Send Response
                    connection_socket.send(client_response)

                    # Close connection
                    connection_socket.close()
                    client_connections.remove(connection_socket)
                except BlockingIOError:
                    continue

                # Connection reset
                except ConnectionResetError:
                    connection_socket.close()
                    dead_connections.append(connection_socket)

                # Keyboard interrupt
                except KeyboardInterrupt:
                    error("KeyboardInterrupt")
                    sys.exit(0)

            # Clean dead connections
            for connection_socket in dead_connections:
                client_connections.remove(connection_socket)

        except KeyboardInterrupt:
            error("KeyboardInterrupt")
            sys.exit(0)
