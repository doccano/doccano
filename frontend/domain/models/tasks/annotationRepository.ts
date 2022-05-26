import ApiService from '@/services/api.service'
import { AnnotationModel } from './interface'

export abstract class AnnotationRepository<T extends AnnotationModel> {
  constructor(private readonly model: any, readonly request = ApiService) {}

  public async list(projectId: string, docId: number): Promise<T[]> {
    const url = this.baseUrl(projectId, docId)
    const response = await this.request.get(url)
    const items: T[] = response.data
    return items.map((item) => this.model.valueOf(item))
  }

  public async create(projectId: string, docId: number, item: T): Promise<void> {
    const url = this.baseUrl(projectId, docId)
    await this.request.post(url, item.toObject())
  }

  public async delete(projectId: string, docId: number, annotationId: number): Promise<void> {
    const url = this.baseUrl(projectId, docId) + `/${annotationId}`
    await this.request.delete(url)
  }

  public async clear(projectId: string, docId: number): Promise<void> {
    const url = this.baseUrl(projectId, docId)
    await this.request.delete(url)
  }

  public async autoLabel(projectId: string, docId: number): Promise<void> {
    const url = `/projects/${projectId}/auto-labeling?example=${docId}`
    await this.request.post(url, {})
  }

  protected baseUrl(projectId: string, docId: number): string {
    return `/projects/${projectId}/examples/${docId}/annotations`
  }
}
