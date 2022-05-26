import { plainToInstance } from 'class-transformer'
import ApiService from '@/services/api.service'
import { TaskStatusRepository } from '@/domain/models/celery/taskStatusRepository'
import { Status } from '@/domain/models/celery/status'

export class APITaskStatusRepository implements TaskStatusRepository {
  constructor(private readonly request = ApiService) {}

  async get(taskId: string): Promise<Status> {
    const url = `/tasks/status/${taskId}`
    const response = await this.request.get(url)
    return plainToInstance(Status, response.data)
  }
}
