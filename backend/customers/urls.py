from django.urls import path

from .views import CustomerDetailsAPIView, CustomerListCreateAPIView

app_name = "customers"

urlpatterns = [
    path('', CustomerListCreateAPIView.as_view(), name='customer-list-create'),
    path('<uuid:pk>/', CustomerDetailsAPIView.as_view(), name='customer-details'),
]