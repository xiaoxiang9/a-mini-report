import type { FeatureEntry } from '../shared/feature.js';

export interface HomeSummary {
  productName: string;
  tagline: string;
  statusText: string;
  features: FeatureEntry[];
}
