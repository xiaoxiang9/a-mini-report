import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  const config = await prisma.platformConfig.upsert({
    where: { id: 1 },
    update: { productName: 'A股投资策略平台', tagline: '用数据，看清每一次市场波动', statusText: '今日市场，保持观察' },
    create: { id: 1, productName: 'A股投资策略平台', tagline: '用数据，看清每一次市场波动', statusText: '今日市场，保持观察' },
  });
  const features = [
    ['daily-review', '每日复盘', '梳理市场脉络，捕捉关键变化', 'available', 1],
    ['stock-tracking', '个股追踪', '持续跟踪关注标的', 'coming-soon', 2],
    ['strategy-selection', '策略选股', '用规则筛选潜在机会', 'coming-soon', 3],
  ] as const;
  for (const [key, title, description, status, sortOrder] of features) {
    await prisma.featureEntry.upsert({
      where: { key },
      update: { title, description, status, sortOrder, platformConfigId: config.id },
      create: { key, title, description, status, sortOrder, platformConfigId: config.id },
    });
  }
}

main().finally(() => prisma.$disconnect());
