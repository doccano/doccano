import { AnnotationModel } from '@/models/tasks/interface'
import { AnnotationRepository } from '@/repositories/tasks/interface'


export class AnnotationApplicationService<T extends AnnotationModel> {
  constructor(
    readonly repository: AnnotationRepository<T>
  ) {}

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
