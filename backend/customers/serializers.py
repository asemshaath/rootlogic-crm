from rest_framework import serializers
from .models import Customer, Address
import re


class CustomerSerializer(serializers.ModelSerializer):
    has_only_primary_address = serializers.BooleanField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'created_at', 'updated_at', 'has_only_primary_address']
        read_only_fields = ('id', 'created_at', 'updated_at', 'num_of_addresses')

    def validate_email(self, value):
        value = value.lower().strip()
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError(
                "Enter a valid email address."
            )

        queryset = Customer.objects.filter(email=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError(
                "A customer with this email already exists."
            )
        
        
        return value
    
    def validate_phone_number(self, value):
        """
        Allow flexible phone format:
        - +1234567890 (international)
        - (123) 456-7890 (US formatted)
        - 123-456-7890
        - 1234567890
        """

        cleaned = re.sub(r'[^\d+]', '', value)

        # Must have at least 10 digits
        digit_count = len(re.sub(r'[^\d]', '', cleaned))
        if digit_count < 10:
            raise serializers.ValidationError(
                "Phone number must have at least 10 digits"
            )
        
        if digit_count > 15:
            raise serializers.ValidationError(
                "Phone number is too long"
            )
        
        queryset = Customer.objects.filter(phone_number=cleaned)
        
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
            
        if queryset.exists():
            raise serializers.ValidationError(
                "A customer with this phone number already exists."
            )
        
        # Store in clean format (keep + if present)
        return cleaned


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