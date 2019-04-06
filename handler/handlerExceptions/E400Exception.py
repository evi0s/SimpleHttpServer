"""400 Exception"""


class E400Exception(Exception):

    def __init__(self, message='Bad Request', code=400, args=('Bad Request',)):
        self.args = args
        self.message = message
        self.code = code
