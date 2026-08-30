import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from app.application.stock_tracking.sync_tracked_stocks import SyncTrackedStocks
from app.infrastructure.config.settings import get_settings
from app.infrastructure.database.session import SessionFactory
from app.infrastructure.stock_tracking.sqlalchemy_repository import SqlAlchemyStockTrackingRepository
from app.infrastructure.stock_tracking.tushare_provider import TushareStockDataProvider


logger = logging.getLogger(__name__)


def build_scheduler(sync_use_case: SyncTrackedStocks) -> BlockingScheduler:
    scheduler = BlockingScheduler(timezone="Asia/Shanghai")
    scheduler.add_job(
        sync_use_case.execute,
        trigger=CronTrigger(hour=17, minute=0, timezone="Asia/Shanghai"),
        id="stock-detail-daily-sync",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )
    return scheduler


def main() -> None:
    settings = get_settings()
    provider = TushareStockDataProvider(settings.tushare_token)
    repository = SqlAlchemyStockTrackingRepository(SessionFactory())
    scheduler = build_scheduler(SyncTrackedStocks(repository, provider))
    logger.info("stock sync scheduler started: 17:00 Asia/Shanghai")
    scheduler.start()


if __name__ == "__main__":
    main()
