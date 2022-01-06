import { Distribution, Progress } from '~/domain/models/statistics/statistics'

export interface StatisticsRepository {
  fetchCategoryDistribution(projectId: string): Promise<Distribution>
  fetchSpanDistribution(projectId: string): Promise<Distribution>
  fetchMemberProgress(projectId: string): Promise<Progress>
}
