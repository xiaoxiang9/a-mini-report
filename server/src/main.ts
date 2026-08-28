import { buildApp } from './interfaces/http/app.js';
import { GetHomeSummary } from './application/home/get-home-summary.js';
import { env } from './infrastructure/config/env.js';
import { checkDatabase } from './infrastructure/database/health-check.js';
import { prisma } from './infrastructure/database/prisma.js';
import { PrismaHomeSummaryRepository } from './infrastructure/platform/prisma-home-summary-repository.js';

const repository = new PrismaHomeSummaryRepository(prisma);
const app = await buildApp({
  homeSummary: new GetHomeSummary(repository),
  checkDatabase: () => checkDatabase(prisma),
});

await app.listen({ port: env.port, host: '0.0.0.0' });
