import type { PrismaClient } from '@prisma/client';
import type { HomeSummaryRepository } from '../../domain/platform/home-summary-repository.js';
import type { HomeSummary } from '../../domain/platform/home-summary.js';

export class PrismaHomeSummaryRepository implements HomeSummaryRepository {
  constructor(private readonly prisma: PrismaClient) {}

  async find(): Promise<HomeSummary> {
    const config = await this.prisma.platformConfig.findFirst({
      include: { features: { orderBy: { sortOrder: 'asc' } } },
      orderBy: { id: 'asc' },
    });
    if (!config) throw new Error('HOME_SUMMARY_NOT_FOUND');
    return {
      productName: config.productName,
      tagline: config.tagline,
      statusText: config.statusText,
      features: [...config.features].sort((a, b) => a.sortOrder - b.sortOrder).map(({ key, title, description, status }) => ({
        key, title, description, status: status as 'available' | 'coming-soon',
      })),
    };
  }
}
