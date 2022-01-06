import ApiService from '@/services/api.service'
import { StatisticsRepository } from '@/domain/models/statistics/statisticsRepository'
import { Distribution, Progress } from '~/domain/models/statistics/statistics'

export class APIStatisticsRepository implements StatisticsRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async fetchCategoryDistribution(projectId: string): Promise<Distribution> {
    const url = `/projects/${projectId}/category-distribution`
    const response = await this.request.get(url)
    return response.data
  }

  async fetchSpanDistribution(projectId: string): Promise<Distribution> {
    const url = `/projects/${projectId}/span-distribution`
    const response = await this.request.get(url)
    return response.data
  }

  async fetchMemberProgress(projectId: string): Promise<Progress> {
    const url = `/projects/${projectId}/member-progress`
    const response = await this.request.get(url)
    return response.data
  }
}
