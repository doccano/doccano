import ApiService from '@/services/api.service'

export class APIParseRepository {
  constructor(private readonly request = ApiService) {}

  async analyze(
    projectId: string,
    format: string,
    task: string,
    uploadIds: number[],
    option: object
  ): Promise<string> {
    const url = `/projects/${projectId}/upload`
    const data = {
      format,
      task,
      uploadIds,
      ...option
    }
    // Add timeout and error handling
    try {
      const response = await this.request.post(url, data, {
        timeout: 60000, // 60 seconds timeout
      })
      return response.data.task_id
    } catch (error) {
      console.error('Upload analysis error:', error)
      throw error
    }
  }

  revert(serverId: string): void {
    const url = `/fp/revert/`
    // Use proper format for DELETE request
    try {
      this.request.delete(url, { data: { id: serverId } })
    } catch (error) {
      console.error('Revert error:', error)
    }
  }
}
