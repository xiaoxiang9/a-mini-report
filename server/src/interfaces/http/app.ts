import Fastify from 'fastify';
import { registerHealthRoute } from './routes/health.js';
import { registerHomeRoute } from './routes/home.js';

export interface AppDependencies {
  homeSummary: { execute: () => Promise<unknown> };
  checkDatabase: () => Promise<'up' | 'down'>;
}

export async function buildApp(dependencies: AppDependencies) {
  const app = Fastify({ logger: false });
  app.setErrorHandler((_error, _request, reply) => {
    reply.code(500).send({ error: 'INTERNAL_SERVER_ERROR' });
  });
  await registerHomeRoute(app, dependencies.homeSummary as never);
  await registerHealthRoute(app, dependencies.checkDatabase);
  return app;
}
