"""500 Exception"""


class E500Exception(Exception):

    def __init__(self, message='Internal Server Error', code=500, args=('Internal Server Error',)):
        self.args = args
        self.message = message
        self.code = code
