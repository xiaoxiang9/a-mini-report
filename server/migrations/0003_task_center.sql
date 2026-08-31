CREATE TABLE IF NOT EXISTS `ScheduledTask` (
    `taskKey` VARCHAR(64) NOT NULL,
    `taskName` VARCHAR(128) NOT NULL,
    `taskType` VARCHAR(64) NOT NULL,
    `enabled` BOOLEAN NOT NULL DEFAULT TRUE,
    `scheduleHour` TINYINT UNSIGNED NOT NULL,
    `scheduleMinute` TINYINT UNSIGNED NOT NULL,
    `timezone` VARCHAR(64) NOT NULL DEFAULT 'Asia/Shanghai',
    `nextRunAt` DATETIME(3) NULL,
    `lastRunAt` DATETIME(3) NULL,
    `lastStatus` VARCHAR(16) NULL,
    `lastSummary` VARCHAR(512) NULL,
    `lastError` VARCHAR(1024) NULL,
    `createdAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `updatedAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    PRIMARY KEY (`taskKey`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `TaskExecutionLog` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `taskKey` VARCHAR(64) NOT NULL,
    `startedAt` DATETIME(3) NOT NULL,
    `finishedAt` DATETIME(3) NULL,
    `durationMs` INT UNSIGNED NULL,
    `status` VARCHAR(16) NOT NULL,
    `successCount` INT NOT NULL DEFAULT 0,
    `failureCount` INT NOT NULL DEFAULT 0,
    `summary` VARCHAR(512) NULL,
    `errorDetail` VARCHAR(1024) NULL,
    PRIMARY KEY (`id`),
    INDEX `TaskExecutionLog_task_started_idx` (`taskKey`, `startedAt`),
    CONSTRAINT `TaskExecutionLog_task_fk` FOREIGN KEY (`taskKey`) REFERENCES `ScheduledTask` (`taskKey`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

INSERT INTO `ScheduledTask` (`taskKey`, `taskName`, `taskType`, `enabled`, `scheduleHour`, `scheduleMinute`, `timezone`)
VALUES ('stock-detail-daily-sync', '股票信息同步', 'stock_sync', TRUE, 17, 0, 'Asia/Shanghai')
ON DUPLICATE KEY UPDATE `taskKey` = `taskKey`;
