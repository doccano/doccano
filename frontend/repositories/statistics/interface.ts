import { Statistics } from '@/models/statistics'

export interface StatisticsRepository {

  fetch(projectId: string): Promise<Statistics>
}
