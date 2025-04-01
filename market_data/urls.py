from django.urls import path
from . import views

urlpatterns = [
    path('status/', views.MarketStatusView.as_view(), name='market-status'),
    path('search/', views.SearchInstrumentsView.as_view(), name='search-instruments'),
    path('instruments/<str:symbol>/history/', views.InstrumentHistoryView.as_view(), name='instrument-history'),
    path('test/', views.TestPolygonAPIView.as_view(), name='test-polygon-api'),
]