from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated


def custom_exception_handler(exc, context):
   
    response = exception_handler(exc, NotAuthenticated)

    # Now add the HTTP status code to the response.
    if response is not None:

        my_response_not_authenticated = { 'success': 0, 'message': 'El token no es válido o ha caducado', 'status': response.status_code }
        response.data = my_response_not_authenticated
    return response