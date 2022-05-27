import { AnnotationApplicationService } from '../annotationApplicationService'
import { Seq2seqDTO } from './seq2seqData'
import { APISeq2seqRepository } from '~/repositories/tasks/seq2seq/apiSeq2seq'
import { Seq2seqLabel } from '~/domain/models/tasks/seq2seq'

export class Seq2seqApplicationService extends AnnotationApplicationService<Seq2seqLabel> {
  constructor(readonly repository: APISeq2seqRepository) {
    super(new APISeq2seqRepository())
  }

  public async list(projectId: string, docId: number): Promise<Seq2seqDTO[]> {
    const items = await this.repository.list(projectId, docId)
    return items.map((item) => new Seq2seqDTO(item))
  }

  public async create(projectId: string, docId: number, text: string): Promise<void> {
    const item = new Seq2seqLabel(0, text, 0)
    await this.repository.create(projectId, docId, item)
  }

  public async changeText(
    projectId: string,
    docId: number,
    annotationId: number,
    text: string
  ): Promise<void> {
    await this.repository.update(projectId, docId, annotationId, text)
  }
}
