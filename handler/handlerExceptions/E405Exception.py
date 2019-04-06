"""405 Exception"""


class E405Exception(Exception):

    def __init__(self, message='Method Not Allowed', code=405, args=('Method Not Allowed',)):
        self.args = args
        self.message = message
        self.code = code
