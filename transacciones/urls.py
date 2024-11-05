from django.urls import path
from .views import TransaccionCreate, recibir_transaccion, TransaccionList, TransaccionDetail

urlpatterns = [
    # URL para recibir y validar una transacción
    path('recibir/', recibir_transaccion, name='recibir_transaccion'),

    # URL para listar todas las transacciones
    path('lista/', TransaccionList.as_view(), name='transaccion-list'),

    # URL para ver el detalle de una transacción específica
    path('<int:Transa_ID>/', TransaccionDetail.as_view(), name='transaccion-detail'),

    # URL para crear una nueva transacción
    path('create/', TransaccionCreate.as_view(), name='transaccion-create'),
]
