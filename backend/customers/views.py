from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from .models import Customer, Address
from .serializers import CustomerSerializer, CustomerListSerializer, AddressListPerCustomerSerializer , AddressSerializer
from rest_framework.views import APIView
from django.db.models import Count, Q
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class CustomerDetailsAPIView(GenericAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
        
    def get(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.has_only_primary_address = customer.addresses.count() == 1
        serializer = self.get_serializer(customer)
        address_serializer = AddressListPerCustomerSerializer(customer.addresses.all(), many=True)
        primary_address = customer.addresses.filter(is_primary=True).first()

        return Response({
            **serializer.data,
            "addresses":{ 
                "count": customer.addresses.count(),
                "data": address_serializer.data,
                "primary_address": AddressListPerCustomerSerializer(primary_address).data if primary_address else None
            },
        }, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        customer = self.get_object()
        serializer = self.get_serializer(customer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        address_serializer = AddressListPerCustomerSerializer(customer.addresses.all(), many=True)
        primary_address = customer.addresses.filter(is_primary=True).first()

        # return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({
            **serializer.data,
            "addresses":{ 
                "count": customer.addresses.count(),
                "data": address_serializer.data,
                "primary_address": AddressListPerCustomerSerializer(primary_address).data if primary_address else None
            },
        }, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomerListCreateAPIView(GenericAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
    def get_queryset(self):
        queryset = Customer.objects.all()
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(phone_number__icontains=search) |
                Q(email__icontains=search)
            )
        
        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(addresses__city__iexact=city).distinct()
        
        state = self.request.query_params.get('state', None)
        if state:
            queryset = queryset.filter(addresses__state__iexact=state).distinct()
        
        pincode = self.request.query_params.get('pincode', None)
        if pincode:
            queryset = queryset.filter(addresses__pincode=pincode).distinct()
        
        queryset = queryset.prefetch_related('addresses')

        for obj in queryset:
            obj.has_only_primary_address = obj.addresses.count() == 1

        return queryset
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CustomerListSerializer(queryset, many=True)
        
        return Response({
            'count': queryset.count(),
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    

class AddressesListAPIView(GenericAPIView):
    queryset = Customer.objects.all()
    serializer_class = AddressSerializer

    def get(self, request, *args, **kwargs):
        customer = self.get_object()
        addresses = customer.addresses.all()
        serializer = self.get_serializer(addresses, many=True)
        
        return Response({
            'count': addresses.count(),
            'data': serializer.data,
            'primary_address': AddressSerializer(customer.addresses.filter(is_primary=True).first()).data if customer.addresses.filter(is_primary=True).exists() else None,
            'primary_address_string': str(customer.addresses.filter(is_primary=True).first()) if customer.addresses.filter(is_primary=True).exists() else None,
        }, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        customer = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=customer)
        
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

class AddressDetailsAPIView(GenericAPIView):
    queryset = Customer.objects.all()
    serializer_class = AddressSerializer

    def get(self, request, *args, **kwargs):
        customer = self.get_object()
        address_id = kwargs.get('address_pk')
        address = customer.addresses.filter(id=address_id).first()
        if not address:
            return Response({'detail': 'Address not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        customer = self.get_object()
        address_id = kwargs.get('address_pk')
        address = customer.addresses.filter(id=address_id).first()
        print(address)
        if not address:
            return Response({'detail': 'Address not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(address, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        customer = self.get_object()
        address_id = kwargs.get('address_pk')
        address = customer.addresses.filter(id=address_id).first()
        if not address:
            return Response({'detail': 'Address not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)