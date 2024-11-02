# transacciones/serializers.py
import datetime
from rest_framework import serializers
from .models import Transaccion

class TransaccionSerializer(serializers.ModelSerializer):
   class Meta:
        model = Transaccion
        fields = [
            'Transa_Tipo',
            'Banco_Oricod',
            'Banco_Orinom',
            'Banco_destcod',
            'Banco_Destnom',
            'Transa_TRN',
            'Fecha_LBTR',
            'Transa_Monto',
            'Transa_Moneda',
            'Cuenta_origen',
            'Cuenta_destino',
            'Transa_comentario',
            'Identif_Benef',
            'Nombre_Benef',
            'Identif_Ctaorigen',
            'Nombre_Ctaorigen',
            'Descrip_Dev',
            'Dev_TRNorg',
        ]


        def validate_Transa_Monto(self, value):
                if value <= 0:
                    raise serializers.ValidationError("El monto debe ser un número positivo.")
                return value
        
        def validate_Fecha(self, value):
            if value > datetime.now().date():
                raise serializers.ValidationError("La fecha no puede ser futura.")
            return value
            

class TransaccionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaccion
        fields = '__all__'  # O selecciona los campos que deseas incluir
