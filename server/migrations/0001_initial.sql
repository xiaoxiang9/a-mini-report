CREATE TABLE IF NOT EXISTS `PlatformConfig` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `productName` VARCHAR(191) NOT NULL,
    `tagline` VARCHAR(191) NOT NULL,
    `statusText` VARCHAR(191) NOT NULL,
    `createdAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `updatedAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `FeatureEntry` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `key` VARCHAR(191) NOT NULL,
    `title` VARCHAR(191) NOT NULL,
    `description` VARCHAR(191) NOT NULL,
    `status` VARCHAR(191) NOT NULL,
    `sortOrder` INTEGER NOT NULL,
    `platformConfigId` INTEGER NOT NULL,
    `createdAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `updatedAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    PRIMARY KEY (`id`),
    UNIQUE INDEX `FeatureEntry_key_key` (`key`),
    INDEX `FeatureEntry_platformConfigId_sortOrder_idx` (`platformConfigId`, `sortOrder`),
    CONSTRAINT `FeatureEntry_platformConfigId_fkey` FOREIGN KEY (`platformConfigId`) REFERENCES `PlatformConfig`(`id`) ON DELETE CASCADE
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

INSERT INTO `PlatformConfig` (`id`, `productName`, `tagline`, `statusText`)
VALUES (1, 'A股投资策略平台', '用数据，看清每一次市场波动', '今日市场，保持观察')
ON DUPLICATE KEY UPDATE `updatedAt` = CURRENT_TIMESTAMP(3);

INSERT INTO `FeatureEntry` (`key`, `title`, `description`, `status`, `sortOrder`, `platformConfigId`)
VALUES
  ('daily-review', '每日复盘', '梳理市场脉络，捕捉关键变化', 'available', 1, 1),
  ('stock-tracking', '个股追踪', '持续跟踪关注标的', 'coming-soon', 2, 1),
  ('strategy-selection', '策略选股', '用规则筛选潜在机会', 'coming-soon', 3, 1)
ON DUPLICATE KEY UPDATE
  `title` = VALUES(`title`), `description` = VALUES(`description`),
  `status` = VALUES(`status`), `sortOrder` = VALUES(`sortOrder`), `platformConfigId` = VALUES(`platformConfigId`);
