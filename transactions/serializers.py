from rest_framework import serializers
from .models import Transaction
from datetime import datetime

class TransactionSerializer(serializers.ModelSerializer):
    formatted_fecha_reg = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['transa_id', 'transa_tipo', 'banco_oricod', 'banco_orinom', 
                  'banco_destcod', 'banco_destnom', 'transa_trn', 
                  'fecha_lbtr', 'transa_monto', 'transa_moneda', 
                  'cuenta_origen', 'cuenta_destino', 'transa_comentario', 
                  'transa_codigo', 'transa_estatus', 'transa_tipocta', 
                  'identif_benef', 'nombre_benef', 'fecha_reg', 
                  'identif_ctaorigen', 'nombre_ctaorigen', 'descrip_dev', 
                  'dev_trnorg', 'formatted_fecha_reg']

    def validate_transa_monto(self, value):
        if value <= 0:
            raise serializers.ValidationError("El monto debe ser mayor que cero.")
        return value

    def validate_fecha_lbtr(self, value):
        if value > datetime.now().date():
            raise serializers.ValidationError("La fecha no puede ser futura.")
        return value

    def get_formatted_fecha_reg(self, obj):
        return obj.fecha_reg.strftime("%Y-%m-%d %H:%M:%S")
