from django.db import models
import datetime
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'organization'
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        self.updated_at = datetime.datetime.now()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('member', 'Member')])
    email = models.EmailField(unique=True)
    USERNAME_FIELD="email"
    REQUIRED_FIELDS=["username"]
    
    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self) -> str:
        return self.email
