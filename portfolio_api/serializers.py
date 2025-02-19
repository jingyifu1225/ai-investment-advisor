from rest_framework import serializers
from .models import Portfolio, Instrument, Metric


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ["performance_data", "updated_at"]


class InstrumentSerializer(serializers.ModelSerializer):
    metric = MetricSerializer(read_only=True)

    class Meta:
        model = Instrument
        fields = ["id", "name", "type", "created_at", "updated_at", "metric"]


class PortfolioSerializer(serializers.ModelSerializer):
    instruments = InstrumentSerializer(many=True, read_only=True)

    class Meta:
        model = Portfolio
        fields = ["id", "name", "created_at", "updated_at", "instruments"]
