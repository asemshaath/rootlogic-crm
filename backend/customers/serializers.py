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


# class AddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         # model = Customer.addresses.through
#         model = Address
#         fields = '__all__'
#         read_only_fields = ('id', 'created_at', 'updated_at')

class AddressListPerCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'address_line1', 'address_line2', 'city', 'state', 'pincode', 'country', 'is_primary',]

class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = ['id', 'address_line1', 'address_line2', 'city', 'state', 'pincode', 'country', 'is_primary', 'created_at', 'updated_at']
        read_only_fields = ('id', 'created_at', 'updated_at')
    

    def validate_pincode(self, value):
        country = self.initial_data.get('country', 'USA')
        
        if country == 'USA':
            # US ZIP: 12345 or 12345-6789
            if not re.match(r'^\d{5}(-\d{4})?$', value):
                raise serializers.ValidationError(
                    "US ZIP code must be format: 12345 or 12345-6789"
                )
                
        return value
    
    def validate_state(self, value):
        country = self.initial_data.get('country', 'USA')
        valid_states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 
                'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 
                'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 
                'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 
                'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 
                'VA', 'WA', 'WV', 'WI', 'WY']

        if country == 'USA':
            if value.upper() not in valid_states:
                raise serializers.ValidationError("Invalid US state code")
            return value.upper()
                
        return value

    def validate(self, attr):

        if not self.instance:
            city = attr.get('city', None)
            country = attr.get('country', 'USA')
            address_line1 = attr.get('address_line1', None)

            if not city or not address_line1 or not country:
                raise serializers.ValidationError(
                    "Address Line1, City, and Country are required."
                )
            
        return attr