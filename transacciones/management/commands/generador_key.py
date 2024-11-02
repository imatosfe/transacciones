# manage/generador_key.py

import secrets
import hashlib
from django.core.management.base import BaseCommand
from transacciones.models import APIKey  # Asegúrate de que la ruta sea correcta

class Command(BaseCommand):
    help = 'Genera una nueva clave y hash para la API'

    def handle(self, *args, **kwargs):
        # Generar una clave aleatoria
        api_key = secrets.token_hex(32)  # Genera una clave aleatoria de 64 caracteres

        # Generar un hash de la clave
        api_hash = hashlib.sha256(api_key.encode()).hexdigest()

        # Guardar en la base de datos
        APIKey.objects.create(key=api_key, hash=api_hash)

        self.stdout.write(self.style.SUCCESS(f'Se generó la clave: {api_key} y el hash: {api_hash}'))
