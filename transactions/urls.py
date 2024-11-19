from django.urls import path
from .views import SecureTransactionList, TransactionListCreate, TransactionList
from .views import SecureTransactionList
from transactions.views import  transaction_list,  transaction_detail
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path
from .views import SecureTransactionList, TransactionListCreate, TransactionList
from . import views
schema_view = get_schema_view(
   openapi.Info(
      title="API de Transacciones",
      default_version='v1',
      description="Documentación de la API de transacciones",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@myapi.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
)

urlpatterns = [
        path('transactions/<int:transa_id>/', transaction_detail, name='transaction-detail'),
    path('api/transactions/', TransactionListCreate.as_view(), name='transaction-list-create'),  # Crear/Listar transacciones
    path('api/transactions/list/', TransactionList.as_view(), name='transaction-list'),  # Listar transacciones
   path('api/transactions/secure/', SecureTransactionList.as_view(), name='secure-transaction-list'),  # Transacciones seguras

path('no-api/transacciones/', transaction_list, name='secure-transaction-list'),  # Transacciones seguras
 path('no-api/create/', views.transaction_create, name='transaction-create'),
  path('no-api/transactions/<int:transa_id>/', transaction_detail, name='transaction-detail'),  # Detalle de transacción
    path('swagger/', schema_view.as_view(), name='schema-swagger-ui'), 
]
