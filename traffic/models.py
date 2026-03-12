from django.db import models


class Intersection(models.Model):
    name = models.CharField(max_length=255, unique=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    location_description = models.TextField(blank=True, null=True)
    zone = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    signal_count = models.IntegerField(default=0)
    camera_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Signal(models.Model):
    PHASE_CHOICES = [
        ('red', 'Red'),
        ('yellow', 'Yellow'),
        ('green', 'Green'),
    ]

    signal_id = models.CharField(max_length=50, unique=True)
    current_phase = models.CharField(max_length=20, choices=PHASE_CHOICES, default='red')
    cycle_time = models.IntegerField()
    green_time = models.IntegerField()
    red_time = models.IntegerField()
    yellow_time = models.IntegerField(default=5)
    controlled_by = models.CharField(max_length=50, default='automated')
    is_active = models.BooleanField(default=True)
    battery_level = models.IntegerField(default=100)
    last_changed = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    intersection = models.ForeignKey(Intersection, on_delete=models.CASCADE)

    class Meta:
        ordering = ['signal_id']

    def __str__(self):
        return self.signal_id


class Route(models.Model):
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    distance_km = models.FloatField()
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_location']
        unique_together = ('start_location', 'end_location')

    def __str__(self):
        return f"{self.start_location} -> {self.end_location}"


class TrafficData(models.Model):
    CONGESTION_CHOICES = [
        ('none', 'None'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('severe', 'Severe'),
    ]

    intersection = models.ForeignKey(Intersection, on_delete=models.CASCADE)
    vehicle_count = models.IntegerField(default=0)
    average_speed = models.FloatField(default=0.0)
    congestion_level = models.CharField(max_length=20, choices=CONGESTION_CHOICES)
    source = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']


class TravelTime(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    distance_km = models.FloatField()
    average_speed_kmh = models.FloatField()
    travel_time_minutes = models.FloatField()
    congestion_level = models.CharField(max_length=50)
    source = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']


class VMSBoard(models.Model):
    board_id = models.IntegerField(unique=True, help_text='Unique board identifier (1-20)')
    vms_player_name = models.CharField(max_length=255, help_text='Location name where board is installed')
    corridor_name = models.CharField(max_length=255, help_text='Corridor name (e.g., Karve chowk to khandoji baba)')
    pair_id = models.IntegerField(help_text='Pair ID from Iteris dashboard')
    location = models.CharField(max_length=255, help_text='Physical location of the board')
    latitude = models.DecimalField(max_digits=10, decimal_places=7, help_text='Latitude coordinate')
    longitude = models.DecimalField(max_digits=10, decimal_places=7, help_text='Longitude coordinate')
    display_time = models.CharField(max_length=100, help_text='Display duration (e.g., 10 seconds every 1 Min)')
    resolution = models.CharField(max_length=20, default='1920x1080', help_text='Display resolution')
    is_active = models.BooleanField(default=True, help_text='Is board currently operational?')
    last_update = models.DateTimeField(auto_now=True, help_text='Last update timestamp')

    class Meta:
        verbose_name = 'VMS Board'
        verbose_name_plural = 'VMS Boards'
        ordering = ['board_id']

    def __str__(self):
        return f"{self.board_id} - {self.location}"
