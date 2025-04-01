import os
import requests
import logging
from datetime import datetime, timedelta
from django.conf import settings

logger = logging.getLogger(__name__)


# api client
class PolygonClient:
    def __init__(self):
        self.api_key = os.environ.get('POLYGON_API_KEY')
        if not self.api_key:
            raise ValueError(
                "Polygon API key is missing.")

        self.base_url = "https://api.polygon.io"
        self.session = requests.Session()

    def _make_request(self, endpoint, params=None):
        if params is None:
            params = {}

        params['apiKey'] = self.api_key
        url = f"{self.base_url}{endpoint}"
        try:
            # GET
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request to Polygon API: {e}")
            raise

    def get_ticker_details(self, symbol):
        endpoint = f"/v3/reference/tickers/{symbol}"
        return self._make_request(endpoint)

    def get_ticker_price(self, symbol):
        endpoint = f"/v2/aggs/ticker/{symbol}/prev"
        return self._make_request(endpoint)

    def get_daily_bars(self, symbol, from_date=None, to_date=None):
        # if no date, return data from past 30 days
        if not from_date:
            from_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not to_date:
            to_date = datetime.now().strftime('%Y-%m-%d')
        endpoint = f"/v2/aggs/ticker/{symbol}/range/1/day/{from_date}/{to_date}"
        return self._make_request(endpoint)

    def get_company_news(self, symbol, limit=10):
        endpoint = f"/v2/reference/news"
        params = {
            'ticker': symbol,
            'limit': limit,
            'order': 'desc'
        }
        return self._make_request(endpoint, params)

    def get_market_status(self):
        endpoint = f"/v1/marketstatus/now"
        return self._make_request(endpoint)

    def search_tickers(self, query, market='stocks', active=True):
        endpoint = f"/v3/reference/tickers"
        params = {
            'search': query,
            'market': market,
            'active': str(active).lower()
        }
        return self._make_request(endpoint, params)

