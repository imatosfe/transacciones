# transacciones/views.py
import requests
from django.conf import settings
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed, NotFound
from .models import Transaccion, APIKey
from .serializers import TransaccionSerializer, TransaccionReadSerializer
import hashlib
import logging
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Configurar el logger
logger = logging.getLogger(__name__)

@swagger_auto_schema(
    method='post',
    operation_description="Consume una API externa y almacena la respuesta en la base de datos. Valida el API Key y el hash antes de guardar la transacción.",
    responses={
        201: TransaccionSerializer,
        401: "API Key o hash no válido.",
        502: "Error al consumir la API externa.",
        503: "Error de conexión con la API externa.",
        500: "Error inesperado en el procesamiento de la transacción."
    }
)
@api_view(['POST'])
def recibir_transaccion(request):
    """
    Vista para consumir una API externa y almacenar la respuesta en la base de datos.
    Valida el API Key y el hash antes de guardar la transacción.
    """
    try:
        api_key = request.headers.get('API-Key')
        if api_key != settings.EXTERNAL_API_KEY:
            logger.warning("API Key no válida.")
            return Response({"detail": "API Key no válida."}, status=status.HTTP_401_UNAUTHORIZED)

        data = f"{settings.EXTERNAL_API_KEY}{settings.EXTERNAL_API_HASH}"
        expected_hash = hashlib.sha256(data.encode()).hexdigest()
        received_hash = request.headers.get('Hash')

        if received_hash != expected_hash:
            logger.warning("Hash no válido.")
            return Response({"detail": "Hash no válido."}, status=status.HTTP_401_UNAUTHORIZED)

        external_response = requests.get(
            settings.EXTERNAL_API_URL,
            headers={
                'API-Key': settings.EXTERNAL_API_KEY,
                'Hash': received_hash
            }
        )

        if external_response.status_code != 200:
            logger.error("Error al consumir la API externa.")
            return Response(
                {"detail": "Error al consumir la API externa."},
                status=status.HTTP_502_BAD_GATEWAY
            )

        data = external_response.json()
        serializer = TransaccionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Transacción guardada con éxito.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error("Error de validación de datos.")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except requests.exceptions.RequestException as e:
        logger.error(f"Error de conexión con la API externa: {e}")
        return Response(
            {"detail": "Error de conexión con la API externa."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except Exception as e:
        logger.exception("Error inesperado en el procesamiento de la transacción.")
        return Response(
            {"detail": "Error inesperado en el procesamiento de la transacción."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class TransaccionList(generics.ListAPIView):
    queryset = Transaccion.objects.all()
    serializer_class = TransaccionReadSerializer

    @swagger_auto_schema(
        operation_description="Lista todas las transacciones. Requiere API Key y hash válidos en los headers.",
        responses={200: TransaccionReadSerializer(many=True), 401: "API key y hash requeridos o inválidos"}
    )
    def get(self, request, *args, **kwargs):
        api_key = request.headers.get('X-Api-Key')
        api_hash = request.headers.get('X-Api-Hash')

        try:
            if not api_key or not api_hash:
                raise AuthenticationFailed('API key y hash requeridos.')

            if not APIKey.objects.filter(key=api_key, hash=api_hash).exists():
                raise AuthenticationFailed('Unauthorized: Invalid API key or hash.')

            return super().get(request, *args, **kwargs)

        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=401)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred: ' + str(e)}, status=500)


class TransaccionDetail(generics.RetrieveAPIView):
    queryset = Transaccion.objects.all()
    serializer_class = TransaccionReadSerializer
    lookup_field = 'Transa_ID'

    @swagger_auto_schema(
        operation_description="Obtiene el detalle de una transacción específica por su ID. Requiere API Key y hash válidos en los headers.",
        responses={200: TransaccionReadSerializer, 401: "API key y hash requeridos o inválidos", 404: "Transacción no encontrada"}
    )
    def get(self, request, *args, **kwargs):
        api_key = request.headers.get('X-Api-Key')
        api_hash = request.headers.get('X-Api-Hash')

        try:
            if not api_key or not api_hash:
                raise AuthenticationFailed('API key y hash requeridos.')

            if not APIKey.objects.filter(key=api_key, hash=api_hash).exists():
                raise AuthenticationFailed('Unauthorized: Invalid API key or hash.')

            transa_id = kwargs.get('Transa_ID')
            if not Transaccion.objects.filter(Transa_ID=transa_id).exists():
                raise NotFound('Transacción no encontrada.')

            return super().get(request, *args, **kwargs)

        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=401)
        except NotFound as e:
            return Response({'error': str(e)}, status=404)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred: ' + str(e)}, status=500)


class TransaccionCreate(generics.CreateAPIView):
    queryset = Transaccion.objects.all()
    serializer_class = TransaccionSerializer

    @swagger_auto_schema(
        operation_description="Crea una nueva transacción. Requiere API Key y hash válidos en los headers.",
        responses={201: TransaccionSerializer, 401: "API key y hash requeridos o inválidos"}
    )
    def post(self, request, *args, **kwargs):
        api_key = request.headers.get('X-Api-Key')
        api_hash = request.headers.get('X-Api-Hash')

        if not api_key or not api_hash:
            return Response({'error': 'API key and hash are required.'}, status=401)

        if not APIKey.objects.filter(key=api_key, hash=api_hash).exists():
            return Response({'error': 'Unauthorized: Invalid API key or hash.'}, status=401)

        return super().post(request, *args, **kwargs)
