export interface ScheduledTask {
  taskKey: string; taskName: string; taskType: string; enabled: boolean;
  scheduleHour: number; scheduleMinute: number; timezone: string;
  nextRunAt: string | null; lastRunAt: string | null; lastStatus: string | null;
  lastSummary: string | null; lastError: string | null;
}
export interface TaskLog { id: number; taskKey: string; startedAt: string; finishedAt: string | null; durationMs: number | null; status: string; successCount: number; failureCount: number; summary: string | null; errorDetail: string | null; }
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:3000';
const adminToken = import.meta.env.VITE_TASK_ADMIN_TOKEN ?? '';
const request = async <T>(path: string, init?: RequestInit): Promise<T> => {
  const response = await fetch(`${apiBaseUrl}${path}`, { ...init, headers: { 'Content-Type': 'application/json', 'X-Task-Admin-Token': adminToken, ...(init?.headers ?? {}) } });
  if (!response.ok) throw new Error(`TASK_API_HTTP_${response.status}`);
  return response.json() as Promise<T>;
};
export const fetchTasks = () => request<ScheduledTask[]>('/api/tasks');
export const updateTask = (taskKey: string, payload: Partial<Pick<ScheduledTask, 'enabled' | 'scheduleHour' | 'scheduleMinute'>>) => request<ScheduledTask>(`/api/tasks/${encodeURIComponent(taskKey)}`, { method: 'PATCH', body: JSON.stringify(payload) });
export const runTask = (taskKey: string) => request<Record<string, unknown>>(`/api/tasks/${encodeURIComponent(taskKey)}/run`, { method: 'POST' });
export const fetchTaskLogs = (taskKey: string) => request<TaskLog[]>(`/api/tasks/${encodeURIComponent(taskKey)}/logs`);
