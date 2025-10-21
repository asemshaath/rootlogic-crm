from django.urls import path

from .views import CustomerDetailsAPIView, CustomerListCreateAPIView, AddressesListAPIView, AddressDetailsAPIView

app_name = "customers"

urlpatterns = [
    path('', CustomerListCreateAPIView.as_view(), name='customer-list-create'),
    path('<uuid:pk>/', CustomerDetailsAPIView.as_view(), name='customer-details'),
    path('<uuid:pk>/addresses/', AddressesListAPIView.as_view(), name='customer-addresses'),
    path('<uuid:pk>/addresses/<uuid:address_pk>/', AddressDetailsAPIView.as_view(), name='customer-address-detail'),
]