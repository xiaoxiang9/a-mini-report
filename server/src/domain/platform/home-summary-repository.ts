import type { HomeSummary } from './home-summary.js';

export interface HomeSummaryRepository {
  find(): Promise<HomeSummary>;
}
