export interface DownloadRepository {
  prepare(projectId: string, format: string): Promise<string>

  download(projectId: string, taskId: string): void
}
