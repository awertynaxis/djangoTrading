import logging
from sys import stdout

from djangoTrading.celery import app

logger = logging.getLogger()
# enabling console output for celery workers
logger.addHandler(logging.StreamHandler(stdout))


@app.task
def make_trade() -> None:
    from trading.services import TradeService

    instance = TradeService()
    instance.make_trade()
