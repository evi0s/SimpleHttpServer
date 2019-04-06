"""Response model"""
import time


class Response:

    # Constructor
    def __init__(self, code=200, message="OK", body=b'', mime='text/plain', length=0):
        self.code = code
        self.message = message
        self.body = body
        self.mime = mime
        self.length = length
        self._res = ''

    def set_body(self, body):
        self.body = body

    def set_length(self, length):
        self.length = length

    def set_mime(self, mime):
        self.mime = mime

    def get_response(self):

        # First line
        self._res += f'HTTP/1.1 {self.code} {self.message}\r\n'

        # Content Type
        self._res += f'Content-Type: {self.mime}\r\n'

        # Content Length
        self._res += f'Content-Length: {self.length}\r\n'

        # Connection
        self._res += 'Connection: closed\r\n'

        # Date
        self._res += f'Date: {time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime())}\r\n'

        # Server
        self._res += 'Server: Simple HTTP Server/0.0.1\r\n'

        # X-Powered-By
        self._res += 'X-Powered-By: Python/3.7'

        # Split Line
        self._res += '\r\n\r\n'

        # Encode response string to bytes
        response = str.encode(self._res)

        # Body
        response += self.body

        return response
