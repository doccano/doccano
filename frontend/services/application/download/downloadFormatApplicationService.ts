import { FormatDTO } from './formatData'
import { DownloadFormatRepository } from '~/domain/models/download/downloadFormatRepository'

export class DownloadFormatApplicationService {
  constructor(private readonly repository: DownloadFormatRepository) {}

  public async list(projectId: string): Promise<FormatDTO[]> {
    const items = await this.repository.list(projectId)
    return items.map((item) => new FormatDTO(item))
  }
}
