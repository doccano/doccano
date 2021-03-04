import ApiService from '@/services/api.service'
import { Statistics } from '@/models/statistics'
import { StatisticsRepository } from './interface'

export class FromApiStatisticsRepository implements StatisticsRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async fetch(projectId: string): Promise<Statistics> {
    const url = `/projects/${projectId}/statistics`
    const response = await this.request.get(url)
    return Statistics.valueOf(response.data)
  }
}
