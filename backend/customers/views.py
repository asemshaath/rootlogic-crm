from django.shortcuts import render
from rest_framework import generics
from .models import Customer
from .serializers import CustomerSerializer

# Create your views here.

class CustomerDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # look_up_field = 'pk'
    

class CustomerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer