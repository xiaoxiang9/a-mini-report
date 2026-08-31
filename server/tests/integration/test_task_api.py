from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.application.task.service import TaskManagementService, TaskRuntimeService
from app.domain.task.models import ScheduledTask, TaskExecutionLog
from app.interfaces.http.routes.tasks import build_tasks_router
from fastapi import FastAPI


class MemoryTasks:
    def __init__(self):
        self.tasks = {"demo": ScheduledTask("demo", "演示", "demo", True, 17, 0)}
        self.logs = []
    def list_tasks(self): return list(self.tasks.values())
    def find_task(self, key): return self.tasks.get(key)
    def save_task(self, task): self.tasks[task.task_key] = task; return task
    def create_log(self, log): log.id = 1; self.logs.append(log); return log
    def finish_log(self, log_id, **values):
        for key, value in values.items(): setattr(self.logs[0], key, value)
        return self.logs[0]
    def list_logs(self, key, limit): return self.logs


def test_task_api_requires_token_and_updates_task() -> None:
    repo = MemoryTasks()
    app = FastAPI()
    app.include_router(build_tasks_router(TaskManagementService(repo), TaskRuntimeService(repo, {"demo": lambda: {}}), "secret"), prefix="/api")
    client = TestClient(app)
    assert client.get("/api/tasks").status_code == 401
    response = client.patch("/api/tasks/demo", headers={"X-Task-Admin-Token": "secret"}, json={"scheduleHour": 8, "scheduleMinute": 15})
    assert response.status_code == 200
    assert response.json()["scheduleHour"] == 8
