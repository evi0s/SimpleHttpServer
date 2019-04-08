"""Multi Thread Server"""
import socket
import sys
from threading import Thread

from utils.debug import *
from handler.handler import handle


def server():

    def connection_handler(connection_socket):
        try:
            # Receive request
            client_request = connection_socket.recv(1024)
            debug(f"Request: {client_request}")

            # Handle request
            client_request = str(client_request, encoding='utf-8')
            client_response = handle(client_request)
            debug("Response: " + str(client_response))

            # Send Response
            connection_socket.send(client_response)

            # Close connection
            connection_socket.close()

        # Connection reset
        except ConnectionResetError:
            connection_socket.close()

        # Keyboard interrupt
        except KeyboardInterrupt:
            error("KeyboardInterrupt")
            sys.exit(0)

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
    debug("Server socket setup finished.")

    while True:
        try:
            # Accept Connection
            connection_socket, client_address = server_socket.accept()
            debug("Client: " + connection_socket.__str__())
            handle_thread = Thread(target=connection_handler, args=(connection_socket, ), daemon=True)
            handle_thread.start()
        except KeyboardInterrupt:
            error("KeyboardInterrupt")
            server_socket.close()
            sys.exit(0)
