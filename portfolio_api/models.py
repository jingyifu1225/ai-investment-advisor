from django.db import models
from django.contrib.auth.models import User

class Portfolio(models.Model):
    user = models.ForeignKey(User, related_name='portfolios', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class Instrument(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='instruments', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.type})"

class Metric(models.Model):
    instrument = models.OneToOneField(Instrument, related_name='metric', on_delete=models.CASCADE)
    performance_data = models.JSONField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Metrics for {self.instrument.name}"