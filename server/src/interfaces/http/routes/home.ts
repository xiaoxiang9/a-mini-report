import type { FastifyInstance } from 'fastify';
import type { GetHomeSummary } from '../../../application/home/get-home-summary.js';

export async function registerHomeRoute(app: FastifyInstance, useCase: Pick<GetHomeSummary, 'execute'>) {
  app.get('/api/home/summary', async (_request, reply) => reply.send(await useCase.execute()));
}
