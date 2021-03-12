import { TextClassificationItem } from '@/models/tasks/text-classification'
import { TextClassificationRepository } from '@/repositories/tasks/text-classification/interface'

export class TextClassificationDTO {
  id: number
  label: number
  user: number

  constructor(item: TextClassificationItem) {
    this.id = item.id
    this.label = item.label
    this.user = item.user
  }
}

export class TextClassificationApplicationService {
  constructor(
    private readonly repository: TextClassificationRepository
  ) {}

  public async list(projectId: string, docId: number): Promise<TextClassificationDTO[]> {
    const items = await this.repository.list(projectId, docId)
    return items.map(item => new TextClassificationDTO(item))
  }

  public async create(projectId: string, docId: number, labelId: number): Promise<void> {
    await this.repository.create(projectId, docId, labelId)
  }

  public async delete(projectId: string, docId: number, annotationId: number): Promise<void> {
    await this.repository.delete(projectId, docId, annotationId)
  }

  public async clear(projectId: string, docId: number): Promise<void> {
    await this.repository.clear(projectId, docId)
  }

  public async autoLabel(projectId: string, docId: number): Promise<void> {
    await this.repository.autoLabel(projectId, docId)
  }
}
