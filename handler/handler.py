"""Handler"""
import os
import mimetypes

from utils.debug import *
from handlerExceptions import *
import config

from Request import *
from Response import *


validMethod = ['GET', 'POST', 'OPTION', 'HEAD', 'PUT', 'PATCH', 'DELETE']


def get_file(path):

    # Index page
    if path == '/':
        path = '/index.html'

    # Dir is forbidden
    if path.endswith('/'):
        raise E403Exception.E403Exception()

    # File information
    file_info = {}
    file_path = config.staticDir + path
    debug(file_path)
    try:
        # Get file content
        with open(file_path, 'rb') as file:
            file_info['content'] = file.read()
            file.close()

        # Get file length
        file_info['length'] = os.path.getsize(file_path)

        # Get file mime
        file_type = mimetypes.guess_type(file_path)
        if file_type[0] is None:
            file_info['mime'] = 'text/plain'
        else:
            debug(file_type[0])
            file_info['mime'] = file_type[0]

        return file_info
    except FileNotFoundError:
        raise E404Exception.E404Exception()


def judge_method(method):

    if method not in validMethod:
        raise E400Exception.E400Exception()

    if method != 'GET':
        raise E405Exception.E405Exception()


def error_page(err):

    error_file_info = {}
    error_file_path = f'{config.defaultErrorDir}/{err.code}.html'
    with open(error_file_path, 'rb') as file:
        error_file_info['content'] = file.read()
        file.close()
    error_file_info['length'] = os.path.getsize(error_file_path)
    error_file_info['mime'] = 'text/html'

    response = Response(code=err.code,
                        message=err.args[0],
                        body=error_file_info['content'],
                        mime=error_file_info['mime'],
                        length=error_file_info['length'])
    return response


def handle(request):
    raw_request = str(request, encoding="utf-8")
    try:
        request_object = Request(raw_request).get_request()
        debug(request_object)
        judge_method(request_object['method'])
        file_info = get_file(request_object['path'])
        response = Response(code=200, message='OK',
                            body=file_info['content'],
                            mime=file_info['mime'],
                            length=file_info['length'])
    except E400Exception.E400Exception as err:
        error(str(err.code) + " " + err.args[0])
        response = error_page(err)
    except E403Exception.E403Exception as err:
        error(str(err.code) + " " + err.args[0])
        response = error_page(err)
    except E404Exception.E404Exception as err:
        error(str(err.code) + " " + err.args[0])
        response = error_page(err)
    except E405Exception.E405Exception as err:
        error(str(err.code) + " " + err.args[0])
        response = error_page(err)
    except E500Exception.E500Exception as err:
        error(str(err.code) + " " + err.args[0])
        response = error_page(err)
    return response.get_response()
