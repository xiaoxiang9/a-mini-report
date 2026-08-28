import type { HomeSummaryRepository } from '../../domain/platform/home-summary-repository.js';
import type { HomeSummary } from '../../domain/platform/home-summary.js';

export class GetHomeSummary {
  constructor(private readonly repository: HomeSummaryRepository) {}

  execute(): Promise<HomeSummary> {
    return this.repository.find();
  }
}
