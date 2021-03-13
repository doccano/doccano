import { FromApiSequenceLabelingRepository } from '@/repositories/tasks/sequenceLabeling/api'
import { AnnotationApplicationService } from './annotationService'
import { SequenceLabelingLabel } from '~/models/tasks/sequenceLabeling'

export class SequenceLabelingDTO {
  id: number
  label: number
  user: number
  startOffset: number
  endOffset: number

  constructor(item: SequenceLabelingLabel) {
    this.id = item.id
    this.label = item.label
    this.user = item.user
    this.startOffset = item.startOffset
    this.endOffset = item.endOffset
  }
}

export class SequenceLabelingApplicationService extends AnnotationApplicationService<SequenceLabelingLabel> {
  constructor(
    readonly repository: FromApiSequenceLabelingRepository
  ) {
    super(new FromApiSequenceLabelingRepository())
  }

  public async list(projectId: string, docId: number): Promise<SequenceLabelingDTO[]> {
    const items = await this.repository.list(projectId, docId)
    return items.map(item => new SequenceLabelingDTO(item))
  }

  public async create(projectId: string, docId: number, labelId: number, startOffset: number, endOffset: number): Promise<void> {
    const item = new SequenceLabelingLabel(0, labelId, 0, startOffset, endOffset)
    await this.repository.create(projectId, docId, item)
  }

  public async changeLabel(projectId: string, docId: number, annotationId: number, labelId: number): Promise<void> {
    await this.repository.update(projectId, docId, annotationId, labelId)
  }
}
