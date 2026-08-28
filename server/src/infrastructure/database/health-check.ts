import type { PrismaClient } from '@prisma/client';

export async function checkDatabase(client: PrismaClient): Promise<'up' | 'down'> {
  try {
    await client.$queryRaw`SELECT 1`;
    return 'up';
  } catch {
    return 'down';
  }
}
