from app.scheduler.stock_sync import build_scheduler


def test_scheduler_runs_daily_at_1700_shanghai() -> None:
    scheduler = build_scheduler(type("Sync", (), {"execute": lambda self: None})())
    jobs = scheduler.get_jobs()

    assert len(jobs) == 1
    assert jobs[0].id == "stock-detail-daily-sync"
    assert str(jobs[0].trigger.timezone) == "Asia/Shanghai"
