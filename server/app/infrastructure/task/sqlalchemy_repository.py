from datetime import datetime

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.domain.task.models import ScheduledTask, TaskExecutionLog
from app.infrastructure.common.converters import safe_int


class SqlAlchemyTaskRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def _task(row: dict) -> ScheduledTask:
        return ScheduledTask(
            task_key=row["taskKey"], task_name=row["taskName"], task_type=row["taskType"], enabled=bool(row["enabled"]),
            schedule_hour=safe_int(row["scheduleHour"]) or 0, schedule_minute=safe_int(row["scheduleMinute"]) or 0, timezone=row["timezone"],
            next_run_at=row["nextRunAt"], last_run_at=row["lastRunAt"], last_status=row["lastStatus"],
            last_summary=row["lastSummary"], last_error=row["lastError"],
        )

    @staticmethod
    def _log(row: dict) -> TaskExecutionLog:
        return TaskExecutionLog(
            id=safe_int(row["id"]) or 0, task_key=row["taskKey"], started_at=row["startedAt"], finished_at=row["finishedAt"],
            duration_ms=row["durationMs"], status=row["status"], success_count=safe_int(row["successCount"]) or 0,
            failure_count=safe_int(row["failureCount"]) or 0, summary=row["summary"], error_detail=row["errorDetail"],
        )

    def list_tasks(self) -> list[ScheduledTask]:
        self.session.rollback()
        rows = self.session.execute(text("SELECT * FROM ScheduledTask ORDER BY taskName, taskKey")).mappings()
        return [self._task(dict(row)) for row in rows]

    def find_task(self, task_key: str) -> ScheduledTask | None:
        self.session.rollback()
        row = self.session.execute(text("SELECT * FROM ScheduledTask WHERE taskKey=:task_key"), {"task_key": task_key}).mappings().first()
        return self._task(dict(row)) if row else None

    def save_task(self, task: ScheduledTask) -> ScheduledTask:
        self.session.execute(text("""
            UPDATE ScheduledTask SET enabled=:enabled, scheduleHour=:hour, scheduleMinute=:minute,
            nextRunAt=:next_run_at, lastRunAt=:last_run_at, lastStatus=:last_status,
            lastSummary=:last_summary, lastError=:last_error WHERE taskKey=:task_key
        """), {"enabled": task.enabled, "hour": task.schedule_hour, "minute": task.schedule_minute,
                "next_run_at": task.next_run_at, "last_run_at": task.last_run_at, "last_status": task.last_status,
                "last_summary": task.last_summary, "last_error": task.last_error, "task_key": task.task_key})
        self.session.commit()
        return self.find_task(task.task_key)  # type: ignore[return-value]

    def create_log(self, log: TaskExecutionLog) -> TaskExecutionLog:
        result = self.session.execute(text("""
            INSERT INTO TaskExecutionLog (taskKey, startedAt, status, successCount, failureCount)
            VALUES (:task_key, :started_at, :status, :success_count, :failure_count)
        """), {"task_key": log.task_key, "started_at": log.started_at, "status": log.status,
                "success_count": log.success_count, "failure_count": log.failure_count})
        self.session.commit()
        log.id = safe_int(result.lastrowid) or 0
        return log

    def finish_log(self, log_id: int, **values: object) -> TaskExecutionLog:
        self.session.execute(text("""
            UPDATE TaskExecutionLog SET finishedAt=:finished_at, durationMs=:duration_ms, status=:status,
            successCount=:success_count, failureCount=:failure_count, summary=:summary, errorDetail=:error_detail
            WHERE id=:id
        """), {"finished_at": values.get("finished_at"), "duration_ms": values.get("duration_ms"),
                "status": values.get("status"), "success_count": values.get("success_count", 0),
                "failure_count": values.get("failure_count", 0), "summary": values.get("summary"),
                "error_detail": values.get("error_detail"), "id": log_id})
        self.session.commit()
        row = self.session.execute(text("SELECT * FROM TaskExecutionLog WHERE id=:id"), {"id": log_id}).mappings().one()
        return self._log(dict(row))

    def list_logs(self, task_key: str, limit: int = 20) -> list[TaskExecutionLog]:
        self.session.rollback()
        rows = self.session.execute(text("""
            SELECT * FROM TaskExecutionLog WHERE taskKey=:task_key ORDER BY startedAt DESC LIMIT :limit
        """), {"task_key": task_key, "limit": min(max(limit, 1), 100)}).mappings()
        return [self._log(dict(row)) for row in rows]
