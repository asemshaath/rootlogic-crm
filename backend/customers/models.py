from django.db import models
from users.models import Organization, User
import uuid

# Create your models here.
class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    # created_by = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = models.DateTimeField(auto_now=True)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.email})"

    class Meta:
        db_table = 'customer'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='USA')
    is_primary = models.BooleanField(default=False)
    

    created_by = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'address'
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
    
    def save(self, *args, **kwargs):
        self.updated_at = models.DateTimeField(auto_now=True)
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"{self.address_line1}, {self.city}, {self.state}, {self.country}"