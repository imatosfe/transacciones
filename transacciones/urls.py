# transacciones/urls.py
from django.urls import path
from .views import TransaccionCreate, recibir_transaccion, TransaccionList, TransaccionDetail

urlpatterns = [
    path('recibir/', recibir_transaccion, name='recibir_transaccion'),
        path('Lista/', TransaccionList.as_view(), name='transaccion-list'),
            path('<int:Transa_ID>/', TransaccionDetail.as_view(), name='transaccion-detail'),
      path('create/', TransaccionCreate.as_view(), name='transaccion-create'),


]
