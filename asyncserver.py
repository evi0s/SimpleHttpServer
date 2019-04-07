import asyncio
import config

from utils.debug import *
from handler.handler import *


def server():

    # Get event loop
    debug('Getting event loop')
    asyncio.get_event_loop()

    class SimpleHTTPServer(asyncio.Protocol):

        transport = object

        def connection_made(self, transport):

            # Accept connection and get client info
            client = transport.get_extra_info('peername')
            debug(f'Connecting from: {client}')

            # Save connection
            self.transport = transport

        def data_received(self, data):

            # Get client data and decode to string
            debug('Getting client request')
            client_request = data.decode()
            debug(f'Request: {client_request}')

            # Handle request
            client_response = handle(client_request)
            debug(f'Response: {client_response}')

            # Response
            self.transport.write(client_response)

            # Close connection
            self.transport.close()

    async def main():

        # Get running event loop
        debug('Getting running event loop')
        running_loop = asyncio.get_running_loop()

        # Create server socket
        debug('Creating server socket')
        async_server = await running_loop.create_server(
            lambda: SimpleHTTPServer(),
            config.host, config.port)

        async with async_server:
            # Put into event loop
            debug('Putting into event loop')
            await async_server.serve_forever()
    try:
        # Start event loop
        asyncio.run(main())
    except KeyboardInterrupt:
        error('KeyboardInterrupt')
