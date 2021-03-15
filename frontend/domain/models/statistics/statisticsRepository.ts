import { Statistics } from '~/domain/models/statistics/statistics'

export interface StatisticsRepository {

  fetch(projectId: string): Promise<Statistics>
}
