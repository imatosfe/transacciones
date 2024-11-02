from django.db import models

class Transaccion(models.Model):
    Transa_ID = models.IntegerField(primary_key=True)
    Transa_Tipo = models.CharField(max_length=3)
    Banco_Oricod = models.CharField(max_length=34)
    Banco_Orinom = models.CharField(max_length=60, null=True, blank=True)
    Banco_destcod = models.CharField(max_length=34)
    Banco_Destnom = models.CharField(max_length=60, null=True, blank=True)
    Transa_TRN = models.CharField(max_length=20)
    Fecha_LBTR = models.DateField()
    Transa_Monto = models.DecimalField(max_digits=13, decimal_places=2)
    Transa_Moneda = models.CharField(max_length=3)
    Cuenta_origen = models.CharField(max_length=34)
    Cuenta_destino = models.CharField(max_length=34)
    Transa_comentario = models.CharField(max_length=210, null=True, blank=True)
    Transa_mensajeerror = models.CharField(max_length=210, null=True, blank=True)
    Transa_Codigo = models.IntegerField(null=True, blank=True)
    Transa_Estatus = models.CharField(max_length=2)
    Transa_Tipocta = models.CharField(max_length=2)
    Identif_Benef = models.CharField(max_length=20, null=True, blank=True)
    Nombre_Benef = models.CharField(max_length=60, null=True, blank=True)
    Fecha_Reg = models.DateTimeField(null=True, blank=True)

    Identif_Ctaorigen = models.CharField(max_length=15, null=True, blank=True)
    Nombre_Ctaorigen = models.CharField(max_length=130, null=True, blank=True)
    Descrip_Dev = models.CharField(max_length=60, null=True, blank=True)
    Dev_TRNorg = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return f"Transacción {self.Transa_ID}"
# models.py

from django.db import models

class APIKey(models.Model):
    key = models.CharField(max_length=255, unique=True)
    hash = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.key
