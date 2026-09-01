export type FeatureStatus = 'available' | 'coming-soon';

export interface FeatureEntry {
  key: string;
  title: string;
  description: string;
  status: FeatureStatus;
}

export interface HomeSummary {
  productName: string;
  tagline: string;
  statusText: string;
  features: FeatureEntry[];
}

export function normalizeHomeSummary(input: unknown): HomeSummary {
  if (!input || typeof input !== 'object') throw new Error('INVALID_HOME_SUMMARY');
  const value = input as Partial<HomeSummary>;
  if (typeof value.productName !== 'string' || typeof value.tagline !== 'string' || typeof value.statusText !== 'string' || !Array.isArray(value.features)) throw new Error('INVALID_HOME_SUMMARY');
  const features = value.features.filter((feature): feature is FeatureEntry => Boolean(feature) && typeof feature === 'object' && typeof feature.key === 'string' && typeof feature.title === 'string' && typeof feature.description === 'string' && (feature.status === 'available' || feature.status === 'coming-soon'));
  if (features.length !== value.features.length) throw new Error('INVALID_HOME_SUMMARY');
  return { productName: value.productName, tagline: value.tagline, statusText: value.statusText, features };
}

export async function fetchHomeSummary(): Promise<HomeSummary> {
  const baseUrl = import.meta.env.VITE_API_BASE_URL ?? '';
  const response = await fetch(`${baseUrl}/api/home/summary`);
  if (!response.ok) throw new Error(`HOME_SUMMARY_HTTP_${response.status}`);
  return normalizeHomeSummary(await response.json());
}
