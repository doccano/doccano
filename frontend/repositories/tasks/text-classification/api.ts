import ApiService from '@/services/api.service'
import { TextClassificationItem } from '@/models/tasks/text-classification'
import { TextClassificationRepository } from './interface'


export class FromApiTextClassificationRepository implements TextClassificationRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  public async list(projectId: string, docId: number): Promise<TextClassificationItem[]> {
    const url = `/projects/${projectId}/docs/${docId}/annotations`
    const response = await this.request.get(url)
    const items: TextClassificationItem[] = response.data
    return items.map(item => TextClassificationItem.valueOf(item))
  }

  public async create(projectId: string, docId: number, labelId: number): Promise<void> {
    const url = `/projects/${projectId}/docs/${docId}/annotations`
    const item = { label: labelId }
    await this.request.post(url, item)
  }

  public async delete(projectId: string, docId: number, annotationId: number): Promise<void> {
    const url = `/projects/${projectId}/docs/${docId}/annotations/${annotationId}`
    await this.request.delete(url)
  }

  public async clear(projectId: string, docId: number): Promise<void> {
    const url = `/projects/${projectId}/docs/${docId}/annotations`
    await this.request.delete(url)
  }
}
