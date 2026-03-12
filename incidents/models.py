from django.db import models
from django.contrib.auth.models import User

class Incident(models.Model):
    """Traffic incident reports (accidents, congestion, etc)"""
    
    TYPE_CHOICES = [
        ('accident', 'Accident'),
        ('congestion', 'Congestion'),
        ('obstruction', 'Obstruction'),
        ('event', 'Event'),
        ('breakdown', 'Breakdown'),
    ]
    
    SEVERITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Very High'),
        (5, 'Critical'),
    ]
    
    incident_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    location = models.CharField(max_length=255, db_index=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    severity = models.IntegerField(choices=SEVERITY_CHOICES)
    description = models.TextField()
    detected_by = models.CharField(max_length=50)  # iteris, vnnox, user
    detected_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False, db_index=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    resolution_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-detected_at']
    
    def __str__(self):
        status = "✓ Resolved" if self.resolved else "🔴 Active"
        return f"{self.incident_type} at {self.location} ({status})"