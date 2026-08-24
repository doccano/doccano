import ApiService from '@/services/api.service'

export class APIDownloadRepository {
  constructor(private readonly request = ApiService) {}

  async prepare(projectId: string, format: string, exportApproved: boolean): Promise<string> {
    const url = `/projects/${projectId}/download`
    const data = {
      format,
      exportApproved
    }
    const response = await this.request.post(url, data)
    return response.data.task_id
  }

  download(projectId: string, taskId: string): void {
    const url = `${process.env.baseUrl}/projects/${projectId}/download?taskId=${taskId}`
    window.location.assign(url)
  }
}
