from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_api_exception_handler(exc, context):
    """Standardized enterprise API exception handler with error codes and request tracing."""
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_data = {
            "success": False,
            "status_code": response.status_code,
            "error_type": exc.__class__.__name__,
            "message": str(exc),
            "details": response.data,
        }
        response.data = custom_data
    else:
        logger.error(f"Unhandled Exception: {exc}", exc_info=True)
        response = Response(
            {
                "success": False,
                "status_code": 500,
                "error_type": "InternalServerError",
                "message": "An unexpected server error occurred. Please contact municipal support.",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
    return response
