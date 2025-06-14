import ApiService from '@/services/api.service'

export abstract class AnnotationRepository<T> {
  labelName = 'dummy'

  constructor(readonly request = ApiService) {}

  public async list(projectId: string, exampleId: number): Promise<T[]> {
    const url = this.baseUrl(projectId, exampleId)
    const response = await this.request.get(url)
    return response.data.map((item: { [key: string]: any }) => this.toModel(item))
  }

  public async find(projectId: string, exampleId: number, labelId: number): Promise<T> {
    const url = `${this.baseUrl(projectId, exampleId)}/${labelId}`
    const response = await this.request.get(url)
    return this.toModel(response.data)
  }

  public async create(projectId: string, exampleId: number, item: T): Promise<void> {
    const url = this.baseUrl(projectId, exampleId)
    const payload = this.toPayload(item)
    await this.request.post(url, payload)
  }

  public async update(projectId: string, exampleId: number, labelId: number, item: T): Promise<T> {
    const url = `${this.baseUrl(projectId, exampleId)}/${labelId}`
    const payload = this.toPayload(item)
    const response = await this.request.patch(url, payload)
    return this.toModel(response.data)
  }

  public async delete(projectId: string, exampleId: number, labelId: number): Promise<void> {
    const url = `${this.baseUrl(projectId, exampleId)}/${labelId}`
    await this.request.delete(url)
  }

  public async clear(projectId: string, exampleId: number): Promise<void> {
    const url = this.baseUrl(projectId, exampleId)
    await this.request.delete(url)
  }

  async bulkDelete(projectId: string, exampleId: number, ids: number[]): Promise<void> {
    const url = `${this.baseUrl(projectId, exampleId)}/${this.labelName}`
    await this.request.delete(url, { ids })
  }

  public async autoLabel(projectId: string, exampleId: number): Promise<void> {
    const url = `/projects/${projectId}/auto-labeling?example=${exampleId}`
    await this.request.post(url, {})
  }

  protected baseUrl(projectId: string, exampleId: number): string {
    return `/projects/${projectId}/examples/${exampleId}/${this.labelName}`
  }

  protected abstract toModel(item: { [key: string]: any }): T

  protected abstract toPayload(item: T): { [key: string]: any }
}
