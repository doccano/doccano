import { AnnotationRepository } from '@/domain/models/tasks/annotationRepository'
import { Seq2seqLabel } from '~/domain/models/tasks/seq2seq'

export class APISeq2seqRepository extends AnnotationRepository<Seq2seqLabel> {
  constructor() {
    super(Seq2seqLabel)
  }

  public async update(projectId: string, docId: number, annotationId: number, text: string) {
    const url = this.baseUrl(projectId, docId) + `/${annotationId}`
    const payload = { text }
    await this.request.patch(url, payload)
  }

  protected baseUrl(projectId: string, docId: number): string {
    return `/projects/${projectId}/examples/${docId}/texts`
  }
}
