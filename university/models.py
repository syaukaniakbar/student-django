# university/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    role = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('mahasiswa', 'Mahasiswa')], default='admin')
    
    def __str__(self):
        return self.username
