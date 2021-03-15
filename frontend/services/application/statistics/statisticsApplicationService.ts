import { StatisticsRepository } from '@/repositories/statistics/interface'
import { StatisticsDTO } from './statisticsData'

export class StatisticsApplicationService {
  constructor(
    private readonly repository: StatisticsRepository
  ) {}

  public async fetchStatistics(
    projectId: string, labelText: string, userText: string, progressLabels: string[]
  ): Promise<StatisticsDTO> {
    const item = await this.repository.fetch(projectId)
    return new StatisticsDTO(item, labelText, userText, progressLabels)
  }
}
