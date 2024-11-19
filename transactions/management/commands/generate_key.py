import os
import django
from django.core.management.base import BaseCommand
from transactions.models import APICredentials
import hashlib

class Command(BaseCommand):
    help = 'Genera una clave y un hash y los guarda en la base de datos'

    def handle(self, *args, **kwargs):
        # Genera la clave y el hash
        key = os.urandom(32).hex()  # Clave de 256 bits
        secret = "lamel"  # Debe ser una clave secreta almacenada de manera segura
        hash_object = hashlib.sha256(f"{key}{secret}".encode())
        hash_value = hash_object.hexdigest()

        # Guarda en la base de datos
        APICredentials.objects.create(key=key, hash_value=hash_value)
        self.stdout.write(self.style.SUCCESS(f'Key: {key}\nHash: {hash_value}'))
        self.stdout.write(self.style.SUCCESS("Credenciales API guardadas en la base de datos."))
