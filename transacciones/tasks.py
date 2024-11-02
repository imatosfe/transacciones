from apptransa.celery import shared_task
import requests
from django.conf import settings
import hashlib
import logging

from transacciones.serializers import TransaccionSerializer

logger = logging.getLogger(__name__)

@shared_task
def recibir_transaccion_task():
    """
    Tarea que consume una API externa y almacena la respuesta en la base de datos.
    """
    try:
        # Validar API Key
        api_key = settings.EXTERNAL_API_KEY
        expected_hash = hashlib.sha256(f"{api_key}{settings.EXTERNAL_API_HASH}".encode()).hexdigest()
        headers = {'API-Key': api_key, 'Hash': expected_hash}

        # Hacer la solicitud a la API externa
        external_response = requests.get(settings.EXTERNAL_API_URL, headers=headers)

        if external_response.status_code != 200:
            logger.error("Error al consumir la API externa.")
            return {"detail": "Error al consumir la API externa."}

        # Convertir la respuesta en JSON
        data = external_response.json()

        # Guardar la transacción en la base de datos (aquí deberías usar tu serializer)
        serializer = TransaccionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Transacción guardada con éxito.")
        else:
            logger.error("Error de validación de datos.")
            return serializer.errors

    except requests.exceptions.RequestException as e:
        logger.error(f"Error de conexión con la API externa: {e}")
        return {"detail": "Error de conexión con la API externa."}
    except Exception as e:
        logger.exception("Error inesperado en el procesamiento de la transacción.")
        return {"detail": "Error inesperado en el procesamiento de la transacción."}
