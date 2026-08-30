# 数据库迁移基线

现有 `PlatformConfig` 和 `FeatureEntry` 表由此前版本创建，本次 Python 服务端迁移只做兼容读取，不重建或清空数据库。

后续新增表结构时，在这里引入 Alembic 迁移版本；生产环境执行迁移前必须先备份 MySQL 数据库，并通过应用发布流程验证。
