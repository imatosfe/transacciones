# transacciones/views.py
import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed, NotFound
from .models import Transaccion
from .serializers import TransaccionSerializer, TransaccionReadSerializer
import hashlib
import logging


from rest_framework import generics

from rest_framework.exceptions import AuthenticationFailed
from .models import Transaccion, APIKey


# Configurar el logger
logger = logging.getLogger(__name__)

@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def recibir_transaccion(request):
    """
    Vista para consumir una API externa y almacenar la respuesta en la base de datos.
    Valida el API Key y el hash antes de guardar la transacción.
    """
    try:
        # Validar API Key en los headers
        api_key = request.headers.get('API-Key')
        if api_key != settings.EXTERNAL_API_KEY:
            logger.warning("API Key no válida.")
            return Response({"detail": "API Key no válida hasta aqui es la prueba."}, status=status.HTTP_401_UNAUTHORIZED)

        # Generar y validar el hash
        data = f"{settings.EXTERNAL_API_KEY}{settings.EXTERNAL_API_HASH}"
        expected_hash = hashlib.sha256(data.encode()).hexdigest()
        received_hash = request.headers.get('Hash')
        
        if received_hash != expected_hash:
            logger.warning("Hash no válido.")
            return Response({"detail": "Hash no válido."}, status=status.HTTP_401_UNAUTHORIZED)

        # Hacer la solicitud a la API externa
        external_response = requests.get(
            settings.EXTERNAL_API_URL,
            headers={
                'API-Key': settings.EXTERNAL_API_KEY,
                'Hash': received_hash
            }
        )

        # Verificar el estado de la respuesta
        if external_response.status_code != 200:
            logger.error("Error al consumir la API externa.")
            return Response(
                {"detail": "Error al consumir la API externa."},
                status=status.HTTP_502_BAD_GATEWAY
            )

        # Convertir la respuesta en JSON
        data = external_response.json()

        # Guardar la transacción en la base de datos
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




from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import Transaccion, APIKey
from .serializers import TransaccionSerializer

class TransaccionList(generics.ListAPIView):
    queryset = Transaccion.objects.all()
    serializer_class = TransaccionReadSerializer

    def get(self, request, *args, **kwargs):
        api_key = request.headers.get('X-Api-Key')
        api_hash = request.headers.get('X-Api-Hash')
      #  api_key = request.headers.get('ec887866f45dfdb074f5256b95dd11986952619857f99d54545ff32060a00224')
       # api_hash = request.headers.get('1b7cd472f6e049351202ecfb519cf54b4bc2e37d87db7f31345ba3c9b611cb49')

        try:
            # Verificar que se recibieron las claves
            if not api_key or not api_hash:
                raise AuthenticationFailed('API key and hash are required.')

            # Verificar la clave y el hash en la base de datos
            if not APIKey.objects.filter(key=api_key, hash=api_hash).exists():
                raise AuthenticationFailed('Unauthorized: Invalid API key or hash.')

            # Si la validación pasa, proceder a obtener las transacciones
            return super().get(request, *args, **kwargs)

        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=401)
        except Exception as e:
            # Manejo de cualquier otra excepción
            return Response({'error': 'An unexpected error occurred: ' + str(e)}, status=500)



class TransaccionDetail(generics.RetrieveAPIView):
    queryset = Transaccion.objects.all()
    serializer_class = TransaccionReadSerializer
    lookup_field = 'Transa_ID'  # El campo para buscar la transacción

    def get(self, request, *args, **kwargs):
        api_key = request.headers.get('X-Api-Key')
        api_hash = request.headers.get('X-Api-Hash')
    #    api_key = request.headers.get('ec887866f45dfdb074f5256b95dd11986952619857f99d54545ff32060a00224')
    #    api_hash = request.headers.get('1b7cd472f6e049351202ecfb519cf54b4bc2e37d87db7f31345ba3c9b611cb49')

        try:
            # Verificar que se recibieron las claves
            if not api_key or not api_hash:
                raise AuthenticationFailed('API key and hash are required.')

            # Verificar la clave y el hash en la base de datos
            if not APIKey.objects.filter(key=api_key, hash=api_hash).exists():
                raise AuthenticationFailed('Unauthorized: Invalid API key or hash.')

            # Obtener el ID de la transacción desde los parámetros
            transa_id = kwargs.get('Transa_ID')
            # Verificar si la transacción existe
            if not Transaccion.objects.filter(Transa_ID=transa_id).exists():
                raise NotFound('Transacción no encontrada.')

            # Proceder a obtener la transacción específica
            return super().get(request, *args, **kwargs)

        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=401)
        except NotFound as e:
            return Response({'error': str(e)}, status=404)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred: ' + str(e)}, status=500)
        




from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import Transaccion, APIKey
from .serializers import TransaccionSerializer

class TransaccionCreate(generics.CreateAPIView):
    queryset = Transaccion.objects.all()
    serializer_class = TransaccionSerializer

    def post(self, request, *args, **kwargs):
        api_key = request.headers.get('X-Api-Key')
        api_hash = request.headers.get('X-Api-Hash')

        # Validar API Key y Hash
        if not api_key or not api_hash:
            return Response({'error': 'API key and hash are required.'}, status=401)

        if not APIKey.objects.filter(key=api_key, hash=api_hash).exists():
            return Response({'error': 'Unauthorized: Invalid API key or hash.'}, status=401)

        # Crear transacción si pasa la validación
        return super().post(request, *args, **kwargs)
