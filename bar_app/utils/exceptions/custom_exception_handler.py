from rest_framework.views import exception_handler, Response
from .custome_exception import CustomException

def custom_exception_handler(exc, context):
    """
    Handles custom exceptions and returns appropriate responses.

    Args:
        exc (Exception): The exception that was raised.
        context (dict): Context information about the exception.

    Returns:
        Response: The response containing the error details.
    """
    response = exception_handler(exc, context)

    if isinstance(exc, CustomException):
        return Response(data=exc.data, status=exc.status)

    if not response:
        response_data = {"detail": str(exc)}
        response = Response(data=response_data, status=500)
    return response
