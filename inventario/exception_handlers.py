from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler para DRF que retorna respuestas API consistentes.
    """
    # Llamar al exception handler por defecto primero
    response = exception_handler(exc, context)

    if response is not None:
        # Agregar estructura personalizada a respuestas de error
        custom_response_data = {
            'success': False,
            'status': response.status_code,
            'message': 'Error en la solicitud',
            'error': response.data
        }

        # Personalizar mensajes según el tipo de error
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            custom_response_data['message'] = 'Datos inválidos. Por favor verifica los campos requeridos.'
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            custom_response_data['message'] = 'Autenticación requerida.'
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            custom_response_data['message'] = 'No tienes permiso para acceder a este recurso.'
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            custom_response_data['message'] = 'El recurso solicitado no fue encontrado.'
        elif response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            custom_response_data['message'] = 'Error interno del servidor.'
            logger.error(f"Error interno: {exc}", exc_info=True)

        response.data = custom_response_data
        return response

    # Si no hay respuesta del handler por defecto, registrar el error
    logger.error(f"Error no manejado: {exc}", exc_info=True)
    return None
