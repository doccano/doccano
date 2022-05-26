import { Status } from './status'

export interface TaskStatusRepository {
  get(taskId: string): Promise<Status>
}
