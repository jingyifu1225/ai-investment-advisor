from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import PortfolioViewSet, InstrumentViewSet

router = DefaultRouter()
router.register(r'portfolios', PortfolioViewSet, basename='portfolio')

portfolio_router = routers.NestedSimpleRouter(router, r'portfolios', lookup='portfolio')
portfolio_router.register(r'instruments', InstrumentViewSet, basename='portfolio-instruments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(portfolio_router.urls)),
]
