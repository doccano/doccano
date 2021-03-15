import { StatisticsDTO } from './statisticsData'
import { StatisticsRepository } from '~/domain/models/statistics/statisticsRepository'

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
