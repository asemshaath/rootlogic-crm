from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import NotFound, ValidationError

def custom_exception_handler(exc, context):
    # First, use DRF's default handler
    response = exception_handler(exc, context)
    
    if response is not None:
        # Format the error response
        custom_response = {
            'error': True,
            'message': str(exc),
            'details': response.data
        }
        response.data = custom_response
                
        return response
    
    # Djano specific exceptions
    if isinstance(exc, Http404):
        return Response(
            {'error': True, 'message': 'Resource not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if isinstance(exc, (DjangoValidationError, ValidationError)):
        return Response(
            {'error': True, 'message': 'Validation error', 'details': str(exc)},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return Response({
        'error': True,
        'message': 'An unexpected error occurred',
        'details': None
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
