SET @sql = IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
     WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'StockDetail' AND COLUMN_NAME = 'historyStartDate') = 0,
    'ALTER TABLE `StockDetail` ADD COLUMN `historyStartDate` DATE NULL',
    'SELECT 1'
);
PREPARE migration_stmt FROM @sql;
EXECUTE migration_stmt;
DEALLOCATE PREPARE migration_stmt;

SET @sql = IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
     WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'StockDetail' AND COLUMN_NAME = 'historyEndDate') = 0,
    'ALTER TABLE `StockDetail` ADD COLUMN `historyEndDate` DATE NULL',
    'SELECT 1'
);
PREPARE migration_stmt FROM @sql;
EXECUTE migration_stmt;
DEALLOCATE PREPARE migration_stmt;

SET @sql = IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
     WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'StockDetail' AND COLUMN_NAME = 'historyCount') = 0,
    'ALTER TABLE `StockDetail` ADD COLUMN `historyCount` INT NOT NULL DEFAULT 0',
    'SELECT 1'
);
PREPARE migration_stmt FROM @sql;
EXECUTE migration_stmt;
DEALLOCATE PREPARE migration_stmt;
