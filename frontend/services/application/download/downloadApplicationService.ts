import { DownloadRepository } from '~/domain/models/download/downloadRepository'

export class DownloadApplicationService {
  constructor(private readonly repository: DownloadRepository) {}

  public async request(
    projectId: string,
    format: string,
    exportApproved: boolean
  ): Promise<string> {
    const item = await this.repository.prepare(projectId, format, exportApproved)
    return item
  }

  public download(projectId: string, taskId: string): void {
    this.repository.download(projectId, taskId)
  }
}
