from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response as DRFResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .market_data_service import MarketDataService


class MarketDataAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = MarketDataService()


class MarketStatusView(MarketDataAPIView):

    def get(self, request):
        status_data = self.service.api_client.get_market_status()
        if status_data:
            return DRFResponse(status_data)
        return DRFResponse({"error": "Failed to retrieve market status"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class SearchInstrumentsView(MarketDataAPIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query or len(query) < 2:
            return DRFResponse({"error": "Search query must be at least 2 characters"},
                               status=status.HTTP_400_BAD_REQUEST)
        results = self.service.search_instruments(query)
        return DRFResponse({"results": results})


class InstrumentHistoryView(MarketDataAPIView):
    def get(self, request, symbol):
        days = int(request.query_params.get('days', 30))
        history = self.service.get_instrument_history(symbol, days)
        if history:
            return DRFResponse({"symbol": symbol, "history": history})
        return DRFResponse({"error": f"Failed to retrieve history for {symbol}"}, status=status.HTTP_404_NOT_FOUND)


class InstrumentDetailsView(MarketDataAPIView):

    def get(self, request, symbol):
        details = self.service.api_client.get_ticker_details(symbol)
        if details:
            return DRFResponse(details)
        return DRFResponse({"error": f"Failed to retrieve details for {symbol}"}, status=status.HTTP_404_NOT_FOUND)


class TestPolygonAPIView(MarketDataAPIView):

    def get(self, request):
        symbol = request.query_params.get('symbol')
        if not symbol:
            return DRFResponse({"error": "Symbol parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        test_type = request.query_params.get('type', 'all')

        try:
            results = {}
            if test_type in ['details', 'all']:
                ticker_details = self.service.api_client.get_ticker_details(symbol)
                results['ticker_details'] = ticker_details
            if test_type in ['price', 'all']:
                results['latest_price'] = self.service.api_client.get_ticker_price(symbol)
            if test_type in ['history', 'all']:
                daily_bars = self.service.api_client.get_daily_bars(symbol)
                results['daily_bars'] = daily_bars
            if test_type in ['news', 'all']:
                news = self.service.api_client.get_company_news(symbol)
                results['company_news'] = news

            return DRFResponse({'success': True, 'symbol': symbol, 'results': results})
        except Exception as e:
            return DRFResponse({'success': False, 'symbol': symbol, 'error': str(e)}, status=500)
