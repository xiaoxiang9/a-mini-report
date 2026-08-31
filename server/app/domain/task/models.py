from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScheduledTask:
    task_key: str
    task_name: str
    task_type: str
    enabled: bool
    schedule_hour: int
    schedule_minute: int
    timezone: str = "Asia/Shanghai"
    next_run_at: datetime | None = None
    last_run_at: datetime | None = None
    last_status: str | None = None
    last_summary: str | None = None
    last_error: str | None = None


@dataclass
class TaskExecutionLog:
    id: int | None
    task_key: str
    started_at: datetime
    finished_at: datetime | None
    duration_ms: int | None
    status: str
    success_count: int = 0
    failure_count: int = 0
    summary: str | None = None
    error_detail: str | None = None
