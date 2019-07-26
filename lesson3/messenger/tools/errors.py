class IncorrectDataReceivedError(Exception):
    def __str__(self):
        return 'Wrong message has been received from the remote machine.'


class ServerError(Exception):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


class NonDictInputError(Exception):
    def __str__(self):
        return 'Argument must be dictionary.'


class ReqFieldMissingError(Exception):
    def __init__(self, missing_field):
        self.missing_field = missing_field

    def __str__(self):
        return f'The field {self.missing_field} is missing in the dictionary.'
