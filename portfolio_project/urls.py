from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


def home_view(request):
    return HttpResponse("Welcome to AI Investment Advisor!")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("portfolio_api.urls")),
    path("", home_view),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('rag/', include('rag_pipeline.urls')),
    path('api/market/', include('market_data.urls')),
]
