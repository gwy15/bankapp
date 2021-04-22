class BankException(Exception):
    pass


class UserDoesNotExistOrWrongPassword(BankException):
    pass


class UsernameTaken(BankException):
    pass
