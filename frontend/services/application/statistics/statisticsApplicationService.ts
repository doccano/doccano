import { StatisticsRepository } from '~/domain/models/statistics/statisticsRepository'
import { Progress, Distribution } from '~/domain/models/statistics/statistics'

export class StatisticsApplicationService {
  constructor(
    private readonly repository: StatisticsRepository
  ) {}

  public async fetchMemberProgress(projectId: string): Promise<Progress> {
    return await this.repository.fetchMemberProgress(projectId)
  }

  public async fetchCategoryDistribution(projectId: string): Promise<Distribution> {
    return await this.repository.fetchCategoryDistribution(projectId)
  }

  public async fetchSpanDistribution(projectId: string): Promise<Distribution> {
    return await this.repository.fetchSpanDistribution(projectId)
  }
}
