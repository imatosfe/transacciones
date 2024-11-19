# transactions/forms.py
from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'transa_id', 'transa_tipo', 'banco_oricod', 'banco_orinom', 
            'banco_destcod', 'banco_destnom', 'transa_trn', 'fecha_lbtr', 
            'transa_monto', 'transa_moneda', 'cuenta_origen', 'cuenta_destino', 
            'transa_comentario', 'transa_mensajeerror', 'transa_codigo', 
            'transa_estatus', 'transa_tipocta', 'identif_benef', 'nombre_benef', 
            'identif_ctaorigen', 'nombre_ctaorigen', 'descrip_dev', 'dev_trnorg'
        ]
        widgets = {
            'fecha_lbtr': forms.DateInput(attrs={'type': 'date'}),
            'transa_monto': forms.NumberInput(attrs={'step': '0.01'}),
        }
