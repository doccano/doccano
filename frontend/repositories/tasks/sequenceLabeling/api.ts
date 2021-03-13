import { AnnotationRepository } from '../interface'
import { SequenceLabelingLabel } from '~/models/tasks/sequenceLabeling'


export class FromApiSequenceLabelingRepository extends AnnotationRepository<SequenceLabelingLabel> {
  constructor() {
    super(SequenceLabelingLabel)
  }

  public async update(projectId: string, docId: number, annotationId: number, labelId: number) {
    const url = this.baseUrl(projectId, docId) + `/${annotationId}`
    const payload = { label: labelId }
    await this.request.patch(url, payload)
  }

  protected baseUrl(projectId: string, docId: number): string {
    return `/projects/${projectId}/docs/${docId}/annotations`
  }
}