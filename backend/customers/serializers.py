from rest_framework import serializers
from .models import Customer, Address


class CustomerSerializer(serializers.ModelSerializer):
    has_only_primary_address = serializers.BooleanField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'created_at', 'updated_at', 'has_only_primary_address']
        read_only_fields = ('id', 'created_at', 'updated_at', 'num_of_addresses')

    def validate_email(self, value):
        # Email validation (Django already validates format)
        if value and not '@' in value:
            raise serializers.ValidationError("Invalid email format")
        return value
    
    def validate_phone_number(self, value):
        # Basic phone number validation
        import re
        if value and not re.match(r'^\+?1?\d{9,15}$', value):
            raise serializers.ValidationError("Invalid phone number format")
        return value


class CustomerListSerializer(serializers.ModelSerializer):
    has_only_primary_address = serializers.BooleanField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'has_only_primary_address']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        # model = Customer.addresses.through
        model = Address
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')