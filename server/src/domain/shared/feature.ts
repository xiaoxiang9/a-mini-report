export type FeatureStatus = 'available' | 'coming-soon';

export interface FeatureEntry {
  key: string;
  title: string;
  description: string;
  status: FeatureStatus;
}
