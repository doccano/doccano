import { AnnotationApplicationService } from '../annotationApplicationService'
import { SequenceLabelingDTO } from './sequenceLabelingData'
import { APISequenceLabelingRepository } from '~/repositories/tasks/sequenceLabeling/apiSequenceLabeling'
import { SequenceLabelingLabel } from '~/domain/models/tasks/sequenceLabeling'

export class SequenceLabelingApplicationService extends AnnotationApplicationService<SequenceLabelingLabel> {
  constructor(
    readonly repository: APISequenceLabelingRepository
  ) {
    super(new APISequenceLabelingRepository())
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
