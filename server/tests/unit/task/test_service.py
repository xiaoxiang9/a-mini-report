from datetime import datetime

import pytest

from app.application.task.service import TaskManagementService, TaskRuntimeService
from app.domain.task.models import ScheduledTask, TaskExecutionLog


class MemoryTasks:
    def __init__(self) -> None:
        self.tasks = {"demo": ScheduledTask("demo", "演示任务", "demo", True, 17, 0)}
        self.logs: list[TaskExecutionLog] = []

    def list_tasks(self): return list(self.tasks.values())
    def find_task(self, task_key): return self.tasks.get(task_key)
    def save_task(self, task): self.tasks[task.task_key] = task; return task
    def create_log(self, log):
        log.id = len(self.logs) + 1; self.logs.append(log); return log
    def finish_log(self, log_id, **values):
        log = self.logs[log_id - 1]
        for key, value in values.items(): setattr(log, key, value)
        return log
    def list_logs(self, task_key, limit): return [x for x in self.logs if x.task_key == task_key][-limit:]


def test_management_updates_schedule_and_enabled_state() -> None:
    repository = MemoryTasks()
    task = TaskManagementService(repository).update("demo", enabled=False, hour=8, minute=30)
    assert task.enabled is False
    assert (task.schedule_hour, task.schedule_minute) == (8, 30)


def test_management_rejects_invalid_time() -> None:
    with pytest.raises(ValueError, match="INVALID_SCHEDULE"):
        TaskManagementService(MemoryTasks()).update("demo", hour=24)


def test_runtime_records_success_and_updates_task() -> None:
    repository = MemoryTasks()
    result = TaskRuntimeService(repository, {"demo": lambda: {"success_count": 2, "failure_count": 0, "summary": "完成 2 项"}}).run("demo")
    assert result["status"] == "success"
    assert repository.logs[0].status == "success"
    assert repository.tasks["demo"].last_summary == "完成 2 项"


def test_runtime_records_failure() -> None:
    repository = MemoryTasks()
    with pytest.raises(RuntimeError, match="boom"):
        TaskRuntimeService(repository, {"demo": lambda: (_ for _ in ()).throw(RuntimeError("boom"))}).run("demo")
    assert repository.logs[0].status == "failed"
    assert repository.tasks["demo"].last_error == "boom"
