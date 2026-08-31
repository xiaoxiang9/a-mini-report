# 全局任务中心与上市以来估值设计

## 目标

将 PE/PB 历史百分位口径改为“股票上市日到当前最新估值交易日”，并建立独立于业务模块的全局任务中心，支持任务列表、启停、时间修改、手动执行、执行记录和执行情况概述。

## 范围

- 当前注册任务：`stock-detail-daily-sync` 股票信息同步。
- 任务中心是平台基础能力，未来每日复盘、策略选股只需注册新的 task handler。
- 第一阶段不做用户体系；管理接口使用环境变量 `TASK_ADMIN_TOKEN` 进行基础保护。
- Web 提供任务管理页面；微信小程序继续专注业务数据，不展示管理控制台。

## DDD 架构

```text
domain/task
  ScheduledTask, TaskExecutionLog, TaskRepository
application/task
  list, update, run, logs, execute
infrastructure/task
  SQLAlchemy repository, APScheduler runtime, handler registry
interfaces/http/routes/tasks.py
  task management API
```

任务领域不依赖股票模块。`TaskHandlerRegistry` 将 `task_type` 映射到处理器，scheduler 只负责触发任务、控制并发和记录日志；具体同步逻辑继续由股票应用服务负责。

## 数据模型

`ScheduledTask` 保存任务配置和最近一次状态：

- `taskKey` 唯一任务标识
- `taskName`、`taskType`
- `enabled`
- `scheduleHour`、`scheduleMinute`、`timezone`
- `nextRunAt`、`lastRunAt`、`lastStatus`
- `lastSummary`、`lastError`
- `createdAt`、`updatedAt`

`TaskExecutionLog` 保存每次执行：

- `id`、`taskKey`
- `startedAt`、`finishedAt`、`durationMs`
- `status`：running、success、failed
- `successCount`、`failureCount`
- `summary`、`errorDetail`

任务启停和时间变更写入数据库；scheduler 仅允许一个实例运行，启动时加载数据库任务，并在管理修改后刷新对应 job。任务不并发执行，执行日志独立落库。

## API 与保护

```text
GET   /api/tasks
PATCH /api/tasks/{task_key}
POST  /api/tasks/{task_key}/run
GET   /api/tasks/{task_key}/logs
```

管理接口要求 `X-Task-Admin-Token` 与 `TASK_ADMIN_TOKEN` 相等；Token 不写入数据库、源码或前端构建产物。未配置 Token 时管理接口返回配置错误，不默认放开公网控制能力。

## 上市以来百分位

Tushare `stock_basic` 提供 `list_date`。同步时以 `list_date` 为历史起点，按日期分段获取 `daily_basic`，合并已有历史、按交易日去重排序，过滤 PE/PB 的空值和非正值，再按有效样本中 `value <= current_value` 的比例计算百分位。若当前值无效，百分位返回 null；不使用 0 代替。

历史记录保存起止日期与样本数量，便于前端解释数据口径和排查数据缺口。

## 前端

Web 任务中心展示任务状态、启用状态、执行时间、上次/下次执行时间、最近执行概述；支持切换启停、修改小时分钟、手动执行和查看最近日志。失败、未配置 Token 和无执行记录均显示可诊断提示。

## 验收标准

- 百分位测试覆盖上市日、分段合并、去重、无效值和空历史。
- 任务领域测试覆盖启停、时间校验、并发保护、成功/失败日志。
- API 测试覆盖 Token 缺失/错误、列表、修改、运行和日志。
- Web 测试和生产构建通过。
- 现有股票、平台配置和历史数据不被删除；迁移可重复执行。
