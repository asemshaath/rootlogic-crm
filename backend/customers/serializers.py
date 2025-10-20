from rest_framework import serializers
from .models import Customer, Address


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        # model = Customer.addresses.through
        model = Address
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')