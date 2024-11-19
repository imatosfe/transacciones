from django.urls import path
from .views import SecureTransactionList, TransactionListCreate, TransactionList
from .views import SecureTransactionList
from transactions.views import  transaction_list,  transaction_detail

from .views import SecureTransactionList, TransactionListCreate, TransactionList
from . import views

urlpatterns = [
        path('transactions/<int:transa_id>/', transaction_detail, name='transaction-detail'),
    path('api/transactions/', TransactionListCreate.as_view(), name='transaction-list-create'),  # Crear/Listar transacciones
    path('api/transactions/list/', TransactionList.as_view(), name='transaction-list'),  # Listar transacciones
   path('api/transactions/secure/', SecureTransactionList.as_view(), name='secure-transaction-list'),  # Transacciones seguras

path('no-api/transacciones/', transaction_list, name='secure-transaction-list'),  # Transacciones seguras
 path('no-api/create/', views.transaction_create, name='transaction-create'),
  path('no-api/transactions/<int:transa_id>/', transaction_detail, name='transaction-detail'),  # Detalle de transacción
   
]
