from rest_framework.exceptions import ValidationError


class ThirdPartyError(Exception):
    pass


class DateIsNotInThefuture(ValidationError):
    def __init__(self, detail=None, code=None):
        self.detail = "you have to specify a time in the future."
        self.code = 400
