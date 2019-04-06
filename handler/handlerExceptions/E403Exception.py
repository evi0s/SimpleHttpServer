"""403 Exception"""


class E403Exception(Exception):

    def __init__(self, message='Forbidden', code=403, args=('Forbidden',)):
        self.args = args
        self.message = message
        self.code = code
