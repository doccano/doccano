import ApiService from '@/services/api.service'
import { Assignment } from '@/domain/models/example/example'

export class APIAssignmentRepository {
  constructor(private readonly request = ApiService) {}

  async assign(projectId: string, exampleId: number, userId: number): Promise<Assignment> {
    const url = `/projects/${projectId}/assignments`
    const payload = { example: exampleId, assignee: userId }
    const response = await this.request.post(url, payload)
    return response.data
  }

  async unassign(projectId: string, assignmentId: string): Promise<void> {
    const url = `/projects/${projectId}/assignments/${assignmentId}`
    await this.request.delete(url)
  }

  async bulkAssign(projectId: string, workloadAllocation: Object): Promise<void> {
    const url = `/projects/${projectId}/assignments/bulk_assign`
    await this.request.post(url, workloadAllocation)
  }

  async reset(projectId: string): Promise<void> {
    const url = `/projects/${projectId}/assignments/reset`
    await this.request.delete(url)
  }
}
