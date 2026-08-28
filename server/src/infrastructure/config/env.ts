import 'dotenv/config';

export const env = {
  databaseUrl: process.env.DATABASE_URL ?? 'mysql://app:app_password@127.0.0.1:3306/a_stock_platform',
  port: Number(process.env.PORT ?? 3000),
  miniProgramApiBaseUrl: process.env.MINI_PROGRAM_API_BASE_URL ?? 'http://127.0.0.1:3000',
};
