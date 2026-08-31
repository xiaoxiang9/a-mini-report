from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, Path
from pydantic import BaseModel, Field

from app.application.task.service import TaskManagementService, TaskRuntimeService
from app.domain.task.models import ScheduledTask, TaskExecutionLog


class UpdateTaskRequest(BaseModel):
    enabled: bool | None = None
    scheduleHour: int | None = Field(default=None, ge=0, le=23)
    scheduleMinute: int | None = Field(default=None, ge=0, le=59)


class TaskResponse(BaseModel):
    taskKey: str
    taskName: str
    taskType: str
    enabled: bool
    scheduleHour: int
    scheduleMinute: int
    timezone: str
    nextRunAt: datetime | None
    lastRunAt: datetime | None
    lastStatus: str | None
    lastSummary: str | None
    lastError: str | None


class LogResponse(BaseModel):
    id: int | None
    taskKey: str
    startedAt: datetime
    finishedAt: datetime | None
    durationMs: int | None
    status: str
    successCount: int
    failureCount: int
    summary: str | None
    errorDetail: str | None


def _task_response(task: ScheduledTask) -> TaskResponse:
    return TaskResponse(taskKey=task.task_key, taskName=task.task_name, taskType=task.task_type, enabled=task.enabled,
                        scheduleHour=task.schedule_hour, scheduleMinute=task.schedule_minute, timezone=task.timezone,
                        nextRunAt=task.next_run_at, lastRunAt=task.last_run_at, lastStatus=task.last_status,
                        lastSummary=task.last_summary, lastError=task.last_error)


def _log_response(log: TaskExecutionLog) -> LogResponse:
    return LogResponse(id=log.id, taskKey=log.task_key, startedAt=log.started_at, finishedAt=log.finished_at,
                       durationMs=log.duration_ms, status=log.status, successCount=log.success_count,
                       failureCount=log.failure_count, summary=log.summary, errorDetail=log.error_detail)


def build_tasks_router(management: TaskManagementService, runtime: TaskRuntimeService,
                       admin_token: str | None) -> APIRouter:
    router = APIRouter()

    def authorize(token: str | None) -> None:
        if not admin_token or token != admin_token:
            raise HTTPException(status_code=401, detail="TASK_ADMIN_UNAUTHORIZED")

    @router.get("/tasks", response_model=list[TaskResponse])
    def list_tasks(x_task_admin_token: Annotated[str | None, Header()] = None) -> list[TaskResponse]:
        authorize(x_task_admin_token)
        return [_task_response(task) for task in management.list()]

    @router.patch("/tasks/{task_key}", response_model=TaskResponse)
    def update_task(payload: UpdateTaskRequest, task_key: Annotated[str, Path(min_length=1, max_length=64)],
                    x_task_admin_token: Annotated[str | None, Header()] = None) -> TaskResponse:
        authorize(x_task_admin_token)
        try:
            return _task_response(management.update(task_key, enabled=payload.enabled, hour=payload.scheduleHour,
                                                    minute=payload.scheduleMinute))
        except LookupError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error

    @router.post("/tasks/{task_key}/run")
    def run_task(task_key: Annotated[str, Path(min_length=1, max_length=64)],
                 x_task_admin_token: Annotated[str | None, Header()] = None) -> dict[str, object]:
        authorize(x_task_admin_token)
        try:
            return runtime.run(task_key)
        except LookupError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        except Exception as error:
            raise HTTPException(status_code=500, detail=str(error) or "TASK_FAILED") from error

    @router.get("/tasks/{task_key}/logs", response_model=list[LogResponse])
    def list_logs(task_key: Annotated[str, Path(min_length=1, max_length=64)],
                  x_task_admin_token: Annotated[str | None, Header()] = None) -> list[LogResponse]:
        authorize(x_task_admin_token)
        if management.repository.find_task(task_key) is None:
            raise HTTPException(status_code=404, detail="TASK_NOT_FOUND")
        return [_log_response(log) for log in management.repository.list_logs(task_key, 50)]

    return router
