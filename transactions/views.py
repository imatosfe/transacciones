import hashlib
import re
import requests
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Transaction
from .serializers import TransactionSerializer
from django.shortcuts import render, get_object_or_404
from rest_framework import permissions
from rest_framework.views import APIView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction
from .forms import TransactionForm
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings
from .models import APICredentials
from django.utils.crypto import constant_time_compare

from .serializers import TransactionSerializer

class TransactionListCreate(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @swagger_auto_schema(
        operation_description="Crea nuevas transacciones desde una API externa",
        responses={
            201: openapi.Response('Transacciones creadas correctamente', TransactionSerializer(many=True)),
            400: 'Error en los datos enviados',
            500: 'Error en el servidor'
        }
    )
    def post(self, request, *args, **kwargs):
        # URL y cabeceras de la API externa
        url = 'URL_DE_LA_API_EXTERNA'
        headers = {
            'Authorization': '35DD67C5oriTheBeutyExpert',
            'Hash': 'OHGSNGIUKM+Y3EISRVBJUZDDXELU4RKXCIFUVNHHRY4+'
        }

        try:
            # Hacer la solicitud a la API externa
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Lanza un error si la respuesta es un código de error

            # Obtener los datos de la respuesta
            transactions_data = response.json()  # Ajusta esto según la estructura de la API externa

            # Si los datos de transacciones están anidados, ajusta el acceso:
            # transactions_data = response.json().get('results', [])  # Ajusta según la estructura

            # Lista para almacenar transacciones que no existían antes
            new_transactions = []

            # Guardar solo las transacciones no duplicadas
            for data in transactions_data:
                # Aquí asumimos que cada transacción tiene un 'transa_id' único
                transa_id = data.get('transa_id')

                # Verificamos si la transacción ya existe en la base de datos usando 'transa_id'
                if not Transaction.objects.filter(transa_id=transa_id).exists():
                    # Si no existe, la creamos
                    serializer = self.get_serializer(data=data)
                    if serializer.is_valid():
                        # Guardamos la transacción
                        serializer.save()
                        new_transactions.append(data)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # Si la transacción ya existe, la ignoramos
                    continue

            # Responder con un mensaje que indique cuántas transacciones fueron creadas
            if new_transactions:
                return Response(
                    {"message": f"{len(new_transactions)} transacciones almacenadas correctamente"},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {"message": "No hay nuevas transacciones para almacenar."},
                    status=status.HTTP_200_OK
                )

        except requests.exceptions.HTTPError as http_err:
            return Response({"error": f"Error HTTP: {http_err}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.RequestException as req_err:
            return Response({"error": f"Error de solicitud: {req_err}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"Ocurrió un error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            # Guardar la nueva transacción
            form.save()
            # Redirigir a la lista de transacciones
            return redirect('transaction-list')
    else:
        # Formulario vacío para la creación de una nueva transacción
        form = TransactionForm()

    return render(request, 'transactions/transaction_create.html', {'form': form})


def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'transactions/transaction_list.html', {'transactions': transactions})

def transaction_detail(request, transa_id):
    transaction = get_object_or_404(Transaction, transa_id=transa_id)
    return render(request, 'transactions/transaction_detail.html', {'transaction': transaction})










# la original
class TransactionReceive(APIView):
    """
    API para recibir transacciones desde un banco y almacenarlas después de verificar autenticación y hash.
    """

    # Valores esperados (recomendado moverlos a variables de entorno)
    EXPECTED_AUTHORIZATION = '35DD67C5oriTheBeutyExpert'
    EXPECTED_HASH = 'OHGSNGIUKM+Y3EISRVBJUZDDXELU4RKXCIFUVNHHRY4+'

    def post(self, request, *args, **kwargs):
        # Validar autorización
        authorization = request.headers.get('Authorization')
        if not constant_time_compare(authorization, self.EXPECTED_AUTHORIZATION):
            return Response({"error": "Autorización no válida."}, status=status.HTTP_403_FORBIDDEN)

        # Validar hash
        received_hash = request.headers.get('Hash')
        if not constant_time_compare(received_hash, self.EXPECTED_HASH):
            return Response({"error": "Hash no válido."}, status=status.HTTP_403_FORBIDDEN)

        # Procesar los datos enviados por el banco
        try:
            transactions_data = request.data  # Datos en formato JSON enviados por el banco

            # Validar y guardar las transacciones
            new_transactions = []
            for data in transactions_data:
                transa_id = data.get('transa_id')
                if not Transaction.objects.filter(transa_id=transa_id).exists():
                    serializer = TransactionSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        new_transactions.append(data)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Responder según las transacciones procesadas
            if new_transactions:
                return Response(
                    {"message": f"{len(new_transactions)} transacciones almacenadas correctamente."},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {"message": "No hay nuevas transacciones para almacenar."},
                    status=status.HTTP_200_OK
                )

        except Exception as e:
            return Response(
                {"error": f"Ocurrió un error al procesar los datos: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class TransactionList(APIView):
    @swagger_auto_schema(
        operation_description="Obtiene todas las transacciones",
        responses={
            200: openapi.Response('Lista de transacciones', TransactionSerializer(many=True)),
        }
    )
    def get(self, request):
        # Obtener todas las transacciones
        transactions = Transaction.objects.all()
        
        # Limpiar el campo 'transa_comentario', eliminando caracteres no numéricos
        for transaction in transactions:
            if transaction.transa_comentario:
                # Solo dejar los números en el campo transa_comentario
                transaction.transa_comentario = re.sub(r'[^0-9]', '', transaction.transa_comentario)
        
        # Serializar las transacciones
        serializer = TransactionSerializer(transactions, many=True)

        # Devolver los datos procesados
        return Response(serializer.data)


    @swagger_auto_schema(
        operation_description="Crea una nueva transacción",
        request_body=TransactionSerializer,
        responses={
            201: openapi.Response('Transacción creada correctamente', TransactionSerializer),
            400: 'Error en los datos enviados',
        }
    )

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class SecureTransactionList(APIView):
    @swagger_auto_schema(
            operation_description="Obtiene todas las transacciones con autenticación API Key y Hash",
            request_headers={
                'X-Api-Key': openapi.Parameter('X-Api-Key', openapi.IN_HEADER, description="Clave API", type=openapi.TYPE_STRING),
                'X-Api-Hash': openapi.Parameter('X-Api-Hash', openapi.IN_HEADER, description="Hash para verificar la seguridad", type=openapi.TYPE_STRING),
            },
            responses={
                200: openapi.Response('Lista de transacciones', TransactionSerializer(many=True)),
                401: 'Unauthorized - Clave o Hash incorrectos',
            }
        )
    def post(self, request):
        key = request.headers.get('X-Api-Key')
        hash_value = request.headers.get('X-Api-Hash')

        # Agrega los prints aquí para depuración
        print(f"Key: {key}")
        print(f"Hash from request: {hash_value}")

        # Obtén las credenciales de la base de datos
        try:
            api_credentials = APICredentials.objects.get(key=key)
        except APICredentials.DoesNotExist:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        # Calcula el hash esperado
        expected_hash = hashlib.sha256(f"{key}{settings.SECRET_KEY}".encode()).hexdigest()
        print(f"Expected hash: {expected_hash}")  # Agrega este print

        if hash_value != expected_hash:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        # Procesa la solicitud si la validación es correcta
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
