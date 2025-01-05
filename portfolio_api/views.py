from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Portfolio
from .serializers import PortfolioSerializer

class PortfolioViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing user portfolios.
    """
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 仅返回当前用户的 portfolio
        return Portfolio.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 创建时自动关联到当前用户
        serializer.save(user=self.request.user)
