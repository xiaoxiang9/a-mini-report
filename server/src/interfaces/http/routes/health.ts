import type { FastifyInstance } from 'fastify';

export async function registerHealthRoute(app: FastifyInstance, checkDatabase: () => Promise<'up' | 'down'>) {
  app.get('/api/health', async (_request, reply) => {
    const database = await checkDatabase();
    const status = database === 'up' ? 'ok' : 'degraded';
    return reply.code(database === 'up' ? 200 : 503).send({ status, database });
  });
}
