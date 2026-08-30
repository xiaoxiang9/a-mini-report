# 个股追踪模块设计

## 目标

为个人使用的 A 股投资策略平台增加公共个股追踪列表：用户可以添加/移除股票，查看列表指标，点击进入个股详情；服务端每天 17:00（Asia/Shanghai）优先通过 Tushare 增量更新数据。

## 产品边界

- 第一阶段只有一个平台级公共列表，不区分用户，不做注册、登录和权限系统。
- 添加股票接受标准证券代码，内部统一为 `600519.SH`、`000001.SZ` 格式；股票不存在或不支持时返回明确错误。
- 列表展示：股票代码、名称、当前/最近收盘价、最近 7 个交易日涨幅、PE-TTM、PE 历史百分位、PB、PB 历史百分位、数据日期。
- 详情页展示列表字段及估值历史序列、数据来源和同步时间。
- 后续加密策略属于独立安全模块；本阶段不存储或暴露策略密钥，也不把“无登录”误认为安全边界。

## DDD 结构

```text
server/app/
├── domain/stock_tracking/
│   ├── models.py
│   ├── repositories.py
│   └── providers.py
├── application/stock_tracking/
│   ├── list_tracked_stocks.py
│   ├── get_stock_detail.py
│   ├── add_tracked_stock.py
│   ├── remove_tracked_stock.py
│   └── sync_tracked_stocks.py
├── infrastructure/stock_tracking/
│   ├── sqlalchemy_repository.py
│   └── tushare_provider.py
└── scheduler/
    └── stock_sync.py
```

领域层只依赖 Python 标准库和协议；Tushare、SQLAlchemy、调度器均属于基础设施适配器。应用层通过仓储和数据提供者端口编排，不把 Tushare DataFrame 或数据库行对象泄露到接口层。

## 数据模型

新增一张 `StockDetail` 表，使用 `ts_code` 作为唯一股票标识，并保存当前追踪状态和可复用的估值历史：

- `ts_code`、`stock_name`、`exchange`
- `is_tracked`
- `current_price`、`change_7d_percent`
- `pe_ttm`、`pe_percentile`、`pb`、`pb_percentile`
- `valuation_history_json`：按日期保存有效 PE/PB 值，用于增量计算百分位
- `latest_trade_date`、`data_source`、`last_synced_at`、`sync_error`
- `created_at`、`updated_at`

百分位计算只使用对应指标的有效正数历史值，按 `<= 当前值` 的比例计算；无历史值时返回 null，不用 0 伪造结果。7 日涨幅按最近 7 个交易日收盘价计算，不按自然日计算。

## Tushare 数据流

使用 `stock_basic` 标准化股票信息，使用 `trade_cal` 找到最近有效交易日，使用 `daily` 获取收盘价并计算 7 日涨幅，使用 `daily_basic` 获取 PE-TTM 和 PB。历史估值按最后同步日期增量读取，按股票分批并在请求间节流；参数、接口错误和权限错误写入同步结果，不盲目重试参数或权限错误。

Tushare Token 只从 `TUSHARE_TOKEN` 环境变量读取，不写入代码、数据库或前端响应。Token 缺失时同步任务跳过并记录原因，列表仍返回上次成功数据及其数据日期。

## API

```text
GET    /api/stocks/tracking
GET    /api/stocks/{ts_code}
POST   /api/stocks/tracking       body: {"ts_code": "600519.SH"}
DELETE /api/stocks/tracking/{ts_code}
POST   /api/stocks/sync
```

删除只取消追踪（`is_tracked = false`），不删除历史数据；重新添加同一股票复用历史数据。同步接口返回成功/失败数量和每只股票的错误摘要，生产环境后续应加管理员认证。

## 调度

生产环境使用独立 scheduler 进程，每天 17:00 按 `Asia/Shanghai` 执行一次。任务先检查是否有新的交易日，再遍历 `is_tracked = true` 的股票；每只股票独立处理，单只失败不阻断其他股票，完成后批量提交成功结果。API 与 scheduler 共享 MySQL，但不共享进程内状态。

## 前端

Web 和微信小程序的个股追踪入口改为列表页；列表项点击进入详情页，添加入口使用股票代码输入，移除操作二次确认。加载、空列表、接口错误和数据滞后状态均有明确提示；金融数据旁展示最新交易日，不把最近收盘价标记为实时价格。

## 验收标准

- 单元测试覆盖标准代码校验、百分位、7 日涨幅和增量同步失败隔离。
- API 测试覆盖列表、详情、添加、移除及错误响应。
- MySQL 迁移可重复执行，不删除现有 `PlatformConfig`、`FeatureEntry` 或既有股票数据。
- 未配置 Tushare Token 时服务仍可启动，任务给出可诊断错误。
- 调度器时区固定为 `Asia/Shanghai`，不依赖服务器系统时区。
