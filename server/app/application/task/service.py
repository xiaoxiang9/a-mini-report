from datetime import datetime, timezone
from typing import Callable

from app.domain.task.models import ScheduledTask, TaskExecutionLog
from app.infrastructure.common.converters import safe_int
from app.domain.task.repositories import TaskRepository


class TaskManagementService:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def list(self) -> list[ScheduledTask]:
        return self.repository.list_tasks()

    def update(self, task_key: str, *, enabled: bool | None = None, hour: int | None = None,
               minute: int | None = None) -> ScheduledTask:
        task = self.repository.find_task(task_key)
        if task is None:
            raise LookupError("TASK_NOT_FOUND")
        if hour is not None and not 0 <= hour <= 23:
            raise ValueError("INVALID_SCHEDULE_HOUR")
        if minute is not None and not 0 <= minute <= 59:
            raise ValueError("INVALID_SCHEDULE_MINUTE")
        if enabled is not None:
            task.enabled = enabled
        if hour is not None:
            task.schedule_hour = hour
        if minute is not None:
            task.schedule_minute = minute
        return self.repository.save_task(task)


class TaskRuntimeService:
    def __init__(self, repository: TaskRepository, handlers: dict[str, Callable[[], dict[str, object]]]) -> None:
        self.repository = repository
        self.handlers = handlers

    def run(self, task_key: str) -> dict[str, object]:
        task = self.repository.find_task(task_key)
        if task is None:
            raise LookupError("TASK_NOT_FOUND")
        handler = self.handlers.get(task.task_type)
        if handler is None:
            raise LookupError("TASK_HANDLER_NOT_FOUND")
        started_at = datetime.now(timezone.utc)
        log = self.repository.create_log(TaskExecutionLog(None, task_key, started_at, None, None, "running"))
        try:
            result = handler()
            finished_at = datetime.now(timezone.utc)
            summary = str(result.get("summary") or self._summary(result))
            values = {
                "finished_at": finished_at, "duration_ms": max(0, safe_int((finished_at - started_at).total_seconds() * 1000) or 0),
                "status": "success" if not result.get("failure_count") else "failed",
                "success_count": safe_int(result.get("success_count", 0)) or 0, "failure_count": safe_int(result.get("failure_count", 0)) or 0,
                "summary": summary,
            }
            self.repository.finish_log(log.id, **values)
            task.last_run_at, task.last_status, task.last_summary, task.last_error = finished_at, values["status"], summary, None
            self.repository.save_task(task)
            return {"task_key": task_key, "status": values["status"], **result}
        except Exception as error:
            finished_at = datetime.now(timezone.utc)
            message = str(error)[:1024] or error.__class__.__name__
            self.repository.finish_log(log.id, finished_at=finished_at,
                                       duration_ms=max(0, safe_int((finished_at - started_at).total_seconds() * 1000) or 0),
                                       status="failed", summary="任务执行失败", error_detail=message)
            task.last_run_at, task.last_status, task.last_summary, task.last_error = finished_at, "failed", "任务执行失败", message
            self.repository.save_task(task)
            raise

    @staticmethod
    def _summary(result: dict[str, object]) -> str:
        return f"成功 {result.get('success_count', 0)} 项，失败 {result.get('failure_count', 0)} 项"
