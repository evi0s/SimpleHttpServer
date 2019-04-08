"""Request model"""
from urllib.parse import unquote
from handlerExceptions import *
from utils.debug import *


class Request:

    # Constructor
    def __init__(self, request):
        self.rawRequest = request
        self.method = Request.set_method(request)
        self.path = Request.set_path(request)
        self.body = Request.set_body(request)
        self.headers = Request.set_headers(request)

    # Set HTTP method
    @staticmethod
    def set_method(request):
        try:
            method = request.split()[0]
        except IndexError:
            raise E400Exception.E400Exception()
        return method

    # Set request path
    @staticmethod
    def set_path(request):
        try:
            path = Request.clean_path(Request.parse_path(request.split()[1]))
        except IndexError:
            raise E400Exception.E400Exception()
        return path

    # Set request body
    @staticmethod
    def set_body(request):
        try:
            body = request.split('\r\n\r\n', 1)[1]
        except IndexError:
            raise E400Exception.E400Exception()
        return body

    # Set request headers
    @staticmethod
    def set_headers(request):
        try:
            header = request.split('\r\n\r\n', 1)[0]
            header_raw_str = header.split('\r\n')[1:]
            header_dict = {}
            for raw_str in header_raw_str:
                header_str = raw_str.split(': ')
                header_dict[header_str[0]] = header_str[1]
        except IndexError:
            raise E400Exception.E400Exception()
        return header_dict

    # URL decode
    @staticmethod
    def parse_path(path):
        return unquote(path)

    # Keep path safe
    @staticmethod
    def clean_path(path):
        try:
            if b'\x00' in path.encode():
                debug("Null char detected")
                raise E400Exception.E400Exception()
            if '..' in path:
                return Request.clean_path(path)
            else:
                return path
        except RecursionError:
            error("Recursion error in cleaning require path!")
            raise E500Exception.E500Exception()

    # Get path
    def get_path(self):
        return self.path

    # Get method
    def get_method(self):
        return self.method

    # Get headers
    def get_headers(self):
        return self.headers

    # Get body
    def get_body(self):
        return self.body

    # Get request object
    def get_request(self):
        request = {
            '_req': self.rawRequest,
            'method': self.method,
            'path': self.path,
            'headers': self.headers,
            'body': self.body
        }
        return request

