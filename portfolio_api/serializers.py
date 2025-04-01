from rest_framework import serializers
from .models import Portfolio, Instrument, PortfolioMetrics


class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = ['id', 'symbol', 'name', 'type', 'quantity', 'purchase_price',
                  'purchase_date']


class PortfolioMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioMetrics
        fields = ['total_value', 'profit_loss', 'profit_loss_percent',
                  'last_updated', 'risk_score']


class PortfolioSerializer(serializers.ModelSerializer):
    instruments = InstrumentSerializer(many=True, read_only=True)
    metrics = PortfolioMetricsSerializer(read_only=True)

    class Meta:
        model = Portfolio
        fields = ['id', 'name', 'description', 'created_at', 'updated_at',
                  'instruments', 'metrics']