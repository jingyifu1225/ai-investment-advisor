# portfolio_api/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Portfolio
from .serializers import PortfolioSerializer
from rest_framework.authentication import SessionAuthentication


class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
