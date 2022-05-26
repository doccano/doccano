import { MetricsRepository } from '~/domain/models/metrics/metricsRepository'
import { Progress, Distribution, MyProgress } from '~/domain/models/metrics/metrics'

export class MetricsApplicationService {
  constructor(private readonly repository: MetricsRepository) {}

  public async fetchMemberProgress(projectId: string): Promise<Progress> {
    return await this.repository.fetchMemberProgress(projectId)
  }

  public async fetchCategoryDistribution(projectId: string): Promise<Distribution> {
    return await this.repository.fetchCategoryDistribution(projectId)
  }

  public async fetchSpanDistribution(projectId: string): Promise<Distribution> {
    return await this.repository.fetchSpanDistribution(projectId)
  }

  public async fetchRelationDistribution(projectId: string): Promise<Distribution> {
    return await this.repository.fetchRelationDistribution(projectId)
  }

  public async fetchMyProgress(projectId: string): Promise<MyProgress> {
    return await this.repository.fetchMyProgress(projectId)
  }
}
