from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code
    if isinstance(exc, IntegrityError) and not response:
        response = Response({
            'error': 'IntegrityError',
            'status_code': status.HTTP_400_BAD_REQUEST
        })
    return response