from celery import shared_task
from .celery import celery_app
import logging
from .market_data_service import MarketDataService

logger = logging.getLogger(__name__)

# task : update data
@celery_app.task
def update_all_market_data():
    service = MarketDataService()
    updated = service.update_all_instruments()
    logger.info(f"Scheduled task: Updated {updated} instruments with market data")
    return updated

@celery_app.task
def update_market_status():
    service = MarketDataService()
    status = service.get_market_status()
    logger.info(f"Scheduled task: Updated market status: {status}")
    return status