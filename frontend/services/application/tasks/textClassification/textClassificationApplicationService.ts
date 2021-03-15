import { AnnotationApplicationService } from '../annotationApplicationService'
import { TextClassificationDTO } from './textClassificationData'
import { TextClassificationItem } from '~/domain/models/tasks/textClassification'

export class TextClassificationApplicationService extends AnnotationApplicationService<TextClassificationItem> {

  public async list(projectId: string, docId: number): Promise<TextClassificationDTO[]> {
    const items = await this.repository.list(projectId, docId)
    return items.map(item => new TextClassificationDTO(item))
  }

  public async create(projectId: string, docId: number, labelId: number): Promise<void> {
    const item = new TextClassificationItem(0, labelId, 0)
    await this.repository.create(projectId, docId, item)
  }
}
