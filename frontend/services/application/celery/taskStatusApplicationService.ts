import { TaskStatusRepository } from '@/domain/models/celery/taskStatusRepository'
import { StatusDTO } from './statusData'

export class TaskStatusApplicationService {
  constructor(private readonly repository: TaskStatusRepository) {}

  public async get(taskId: string): Promise<StatusDTO> {
    const item = await this.repository.get(taskId)
    return new StatusDTO(item)
  }
}
