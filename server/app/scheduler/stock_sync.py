import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from app.application.stock_tracking.sync_tracked_stocks import SyncTrackedStocks
from app.infrastructure.config.settings import get_settings
from app.infrastructure.database.session import SessionFactory
from app.infrastructure.stock_tracking.sqlalchemy_repository import SqlAlchemyStockTrackingRepository
from app.infrastructure.stock_tracking.tushare_provider import TushareStockDataProvider
from app.application.task.service import TaskRuntimeService
from app.infrastructure.task.sqlalchemy_repository import SqlAlchemyTaskRepository


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


def build_global_scheduler(runtime: TaskRuntimeService, repository: SqlAlchemyTaskRepository) -> BlockingScheduler:
    scheduler = BlockingScheduler(timezone="Asia/Shanghai")

    def refresh_jobs() -> None:
        configured = {task.task_key: task for task in repository.list_tasks() if task.enabled}
        for job in scheduler.get_jobs():
            if job.id != "task-config-refresh" and job.id not in configured:
                scheduler.remove_job(job.id)
        for task in configured.values():
            job = scheduler.add_job(
                lambda key=task.task_key: runtime.run(key),
                trigger=CronTrigger(hour=task.schedule_hour, minute=task.schedule_minute, timezone=task.timezone),
                id=task.task_key, replace_existing=True, max_instances=1, coalesce=True,
            )
            # APScheduler does not expose next_run_time while jobs are pending
            # before scheduler.start(); the 30-second refresh persists it later.
            if scheduler.running:
                task.next_run_at = job.next_run_time
                repository.save_task(task)

    refresh_jobs()
    scheduler.add_job(refresh_jobs, trigger=IntervalTrigger(seconds=30), id="task-config-refresh", replace_existing=True)
    return scheduler


def main() -> None:
    settings = get_settings()
    provider = TushareStockDataProvider(settings.tushare_token)
    stock_repository = SqlAlchemyStockTrackingRepository(SessionFactory())
    task_repository = SqlAlchemyTaskRepository(SessionFactory())
    runtime = TaskRuntimeService(task_repository, {"stock_sync": SyncTrackedStocks(stock_repository, provider).execute})
    scheduler = build_global_scheduler(runtime, task_repository)
    logger.info("global task scheduler started")
    scheduler.start()


if __name__ == "__main__":
    main()
