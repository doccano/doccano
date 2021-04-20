export interface DownloadRepository {
  prepare(projectId: string, format: string, exportApproved: boolean): Promise<string>

  download(projectId: string, taskId: string): void
}
