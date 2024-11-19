from django.db import models

class Transaction(models.Model):
    transa_id = models.IntegerField()
    transa_tipo = models.CharField(max_length=3)
    banco_oricod = models.CharField(max_length=34)
    banco_orinom = models.CharField(max_length=60, null=True, blank=True)
    banco_destcod = models.CharField(max_length=34)
    banco_destnom = models.CharField(max_length=60, null=True, blank=True)
    transa_trn = models.CharField(max_length=20)
    fecha_lbtr = models.DateField()
    transa_monto = models.DecimalField(max_digits=13, decimal_places=2)
    transa_moneda = models.CharField(max_length=3)
    cuenta_origen = models.CharField(max_length=34)
    cuenta_destino = models.CharField(max_length=34)
    transa_comentario = models.CharField(max_length=210, null=True, blank=True)
    transa_mensajeerror = models.CharField(max_length=210, null=True, blank=True)
    transa_codigo = models.IntegerField(null=True, blank=True)
    transa_estatus = models.CharField(max_length=2)
    transa_tipocta = models.CharField(max_length=2)
    identif_benef = models.CharField(max_length=20, null=True, blank=True)
    nombre_benef = models.CharField(max_length=60, null=True, blank=True)
    fecha_reg = models.DateTimeField()
    identif_ctaorigen = models.CharField(max_length=15, null=True, blank=True)
    nombre_ctaorigen = models.CharField(max_length=130, null=True, blank=True)
    descrip_dev = models.CharField(max_length=60, null=True, blank=True)
    dev_trnorg = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return self.transa_trn




class APICredentials(models.Model):
    key = models.CharField(max_length=64, unique=True)
    hash_value = models.CharField(max_length=64)

    def __str__(self):
        return self.key
