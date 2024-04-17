from rest_framework import status as stat
from bar_app.utils.exceptions import CustomException

class UnknownParamException(CustomException):
    code = stat.HTTP_400_BAD_REQUEST
    status = stat.HTTP_400_BAD_REQUEST
    message = "Unknown parameter"
