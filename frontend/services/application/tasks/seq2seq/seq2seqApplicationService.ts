import { AnnotationApplicationService } from '../annotationApplicationService'
import { Seq2seqDTO } from './seq2seqData'
import { TextLabel } from '@/domain/models/tasks/textLabel'

export class Seq2seqApplicationService extends AnnotationApplicationService<TextLabel> {
  public async list(projectId: string, exampleId: number): Promise<Seq2seqDTO[]> {
    const items = await this.repository.list(projectId, exampleId)
    return items.map((item) => new Seq2seqDTO(item))
  }

  public async create(projectId: string, exampleId: number, text: string): Promise<void> {
    const item = new TextLabel(0, text, 0)
    await this.repository.create(projectId, exampleId, item)
  }

  public async changeText(
    projectId: string,
    exampleId: number,
    labelId: number,
    text: string
  ): Promise<void> {
    const textLabel = await this.repository.find(projectId, exampleId, labelId)
    textLabel.updateText(text)
    await this.repository.update(projectId, exampleId, labelId, textLabel)
  }
}
