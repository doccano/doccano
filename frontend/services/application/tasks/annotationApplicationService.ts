import { AnnotationRepository } from '~/domain/models/tasks/annotationRepository'
import { AnnotationModel } from '~/domain/models/tasks/interface'


export class AnnotationApplicationService<T extends AnnotationModel> {
  constructor(
    readonly repository: AnnotationRepository<T>
  ) {}

  public async delete(projectId: string, docId: number, annotationId: number): Promise<void> {
    try {
      await this.repository.delete(projectId, docId, annotationId)
    } catch(e) {
      console.log(e.response.data.detail)
    }
  }

  public async clear(projectId: string, docId: number): Promise<void> {
    await this.repository.clear(projectId, docId)
  }

  public async autoLabel(projectId: string, docId: number): Promise<void> {
    await this.repository.autoLabel(projectId, docId)
  }
}
