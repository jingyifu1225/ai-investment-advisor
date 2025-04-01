from django.db import models
from django.contrib.auth.models import User


class Portfolio(models.Model):
    user = models.ForeignKey(User, related_name='portfolios', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Instrument(models.Model):
    INSTRUMENT_TYPES = (
        ('stock', 'Stock'),
        ('bond', 'Bond'),
        ('etf', 'ETF'),
        ('fund', 'Fund'),
        ('crypto', 'Cryptocurrency'),
    )

    portfolio = models.ForeignKey(Portfolio, related_name='instruments', on_delete=models.CASCADE)
    symbol = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=INSTRUMENT_TYPES)
    quantity = models.DecimalField(max_digits=15, decimal_places=6, default=0)
    purchase_price = models.DecimalField(max_digits=15, decimal_places=6, default=0)
    purchase_date = models.DateField(null=True, blank=True)


    def __str__(self):
        return f"{self.symbol} - {self.name}"


class PortfolioMetrics(models.Model):
    portfolio = models.OneToOneField(Portfolio, related_name='metrics', on_delete=models.CASCADE)
    total_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    profit_loss = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    profit_loss_percent = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)
    risk_score = models.IntegerField(default=0)

    def __str__(self):
        return f"Metrics for {self.portfolio.name}"