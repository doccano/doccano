import { plainToInstance } from 'class-transformer'
import { Status } from '@/domain/models/celery/status'
import ApiService from '@/services/api.service'

export class APITaskStatusRepository {
  constructor(private readonly request = ApiService) {}

  async get(taskId: string): Promise<Status> {
    const url = `/tasks/status/${taskId}`
    const response = await this.request.get(url)
    return plainToInstance(Status, response.data)
  }
}
