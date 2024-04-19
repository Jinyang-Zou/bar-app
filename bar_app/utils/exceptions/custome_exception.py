from rest_framework import status

class CustomException(Exception):
    """
    Custom exception class for handling API errors.
    """
    _default_code = 400
    default_message = None

    def __init__(
        self,
        message = "",
        status_code = status.HTTP_400_BAD_REQUEST,
        data = None,
        code = _default_code,
    ):
        self.code = code
        self.status = status_code
        self.message = message
        if not data:
            self.data = {"detail": message}
        else:
            self.data = data

    def __str__(self):
        return str(self.code) + self.message
