ALTER TABLE `StockDetail`
    ADD COLUMN `historyStartDate` DATE NULL,
    ADD COLUMN `historyEndDate` DATE NULL,
    ADD COLUMN `historyCount` INT NOT NULL DEFAULT 0;
