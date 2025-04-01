import logging
from datetime import datetime
from .polygon_client import PolygonClient
from portfolio_api.models import Instrument

logger = logging.getLogger(__name__)


class MarketDataService:

    def __init__(self, api_client=None):
        self.api_client = api_client or PolygonClient()

    def update_instrument_data(self, instrument):
        try:
            ticker = instrument.symbol
            price_data = self.api_client.get_ticker_price(ticker)

            if 'results' in price_data and price_data['results']:
                result = price_data['results'][0]

                instrument.current_price = result.get('c', instrument.current_price)  # 收盘价
                instrument.daily_high = result.get('h', None)  # 最高价
                instrument.daily_low = result.get('l', None)  # 最低价
                instrument.daily_open = result.get('o', None)  # 开盘价
                instrument.daily_volume = result.get('v', None)  # 成交量
                instrument.last_updated = datetime.now()
                instrument.save()

                logger.info(f"Updated market data for {ticker}")
                return True
            else:
                logger.warning(f"No price data found for {ticker}")
                return False

        except Exception as e:
            logger.error(f"Error updating market data for {instrument.symbol}: {str(e)}")
            return False

    def update_all_instruments(self):
        # Get all instruments
        instruments = Instrument.objects.all()
        updated_count = 0

        for instrument in instruments:
            if self.update_instrument_data(instrument):
                updated_count += 1

        logger.info(f"Updated market data for {updated_count} out of {len(instruments)} instruments")
        return updated_count

    def search_instruments(self, query):
        try:
            search_results = self.api_client.search_tickers(query)

            formatted_results = []
            if 'results' in search_results and search_results['results']:
                for result in search_results['results']:
                    formatted_results.append({
                        'symbol': result.get('ticker'),
                        'name': result.get('name'),
                        'market': result.get('market'),
                        'locale': result.get('locale'),
                        'primary_exchange': result.get('primary_exchange'),
                        'type': result.get('type'),
                        'currency': result.get('currency_name')
                    })

            return formatted_results
        except Exception as e:
            logger.error(f"Error searching for instruments: {str(e)}")
            return []

    def get_instrument_history(self, symbol, days=30):
        try:
            history_data = self.api_client.get_daily_bars(symbol)
            formatted_history = []
            if 'results' in history_data and history_data['results']:
                for bar in history_data['results']:
                    formatted_history.append({
                        'date': datetime.fromtimestamp(bar['t'] / 1000).strftime('%Y-%m-%d'),
                        'open': bar.get('o'),
                        'high': bar.get('h'),
                        'low': bar.get('l'),
                        'close': bar.get('c'),
                        'volume': bar.get('v')
                    })

            return formatted_history
        except Exception as e:
            logger.error(f"Error getting history for {symbol}: {str(e)}")
            return []

    def get_market_status(self):
        try:
            status_data = self.api_client.get_market_status()
            logger.info(f"Got market status: {status_data}")
            return status_data
        except Exception as e:
            logger.error(f"Error getting market status: {str(e)}")
            return None
