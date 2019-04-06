"""404 Exception"""


class E404Exception(Exception):

    def __init__(self, message='Not Found', code=404, args=('Not Found',)):
        self.args = args
        self.message = message
        self.code = code
