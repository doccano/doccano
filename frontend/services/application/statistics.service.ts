import { Statistics } from '@/models/statistics'
import { StatisticsRepository } from '@/repositories/statistics/interface'

export class StatisticsDTO {
  label: object
  user: object
  progress: object

  constructor(item: Statistics, labelText: string, userText: string, progressLabels: string[]) {
    this.label = item.labelStats(labelText)
    this.user = item.userStats(userText)
    this.progress = item.progress(progressLabels)
  }
}

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
