from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Extended user profile with roles.
    WHY: Django's User has username, email, password
    But we need: role, phone, department
    """
    
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('operator', 'Operator'),
        ('viewer', 'Viewer'),
    ]
    
    # Link to Django's User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # User's role
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='viewer'
    )
    
    # Optional phone
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Department
    department = models.CharField(max_length=100, blank=True, null=True)
    
    # Active status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} ({self.role})"