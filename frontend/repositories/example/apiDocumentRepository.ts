import ApiService from '@/services/api.service'
import { ExampleRepository, SearchOption } from '@/domain/models/example/exampleRepository'
import { ExampleItem, ExampleItemList } from '@/domain/models/example/example'

function toModel(item: { [key: string]: any }): ExampleItem {
  return new ExampleItem(
    item.id,
    item.text,
    item.meta,
    item.annotation_approver,
    item.comment_count,
    item.filename,
    item.is_confirmed,
    item.upload_name
  )
}

function toPayload(item: ExampleItem): { [key: string]: any } {
  return {
    id: item.id,
    text: item.text,
    meta: item.meta,
    annotation_approver: item.annotationApprover,
    comment_count: item.commentCount
  }
}

export class APIExampleRepository implements ExampleRepository {
  constructor(private readonly request = ApiService) {}

  async list(
    projectId: string,
    { limit = '10', offset = '0', q = '', isChecked = '' }: SearchOption
  ): Promise<ExampleItemList> {
    const url = `/projects/${projectId}/examples?limit=${limit}&offset=${offset}&q=${q}&confirmed=${isChecked}`
    const response = await this.request.get(url)
    return new ExampleItemList(
      response.data.count,
      response.data.next,
      response.data.previous,
      response.data.results.map((item: { [key: string]: any }) => toModel(item))
    )
  }

  async create(projectId: string, item: ExampleItem): Promise<ExampleItem> {
    const url = `/projects/${projectId}/examples`
    const payload = toPayload(item)
    const response = await this.request.post(url, payload)
    return toModel(response.data)
  }

  async update(projectId: string, item: ExampleItem): Promise<ExampleItem> {
    const url = `/projects/${projectId}/examples/${item.id}`
    const payload = toPayload(item)
    const response = await this.request.patch(url, payload)
    return toModel(response.data)
  }

  async bulkDelete(projectId: string, ids: number[]): Promise<void> {
    const url = `/projects/${projectId}/examples`
    await this.request.delete(url, { ids })
  }

  async deleteAll(projectId: string): Promise<void> {
    const url = `/projects/${projectId}/examples`
    await this.request.delete(url)
  }

  async findById(projectId: string, exampleId: number): Promise<ExampleItem> {
    const url = `/projects/${projectId}/examples/${exampleId}`
    const response = await this.request.get(url)
    return toModel(response.data)
  }

  async confirm(projectId: string, exampleId: number): Promise<void> {
    const url = `/projects/${projectId}/examples/${exampleId}/states`
    await this.request.post(url, {})
  }
}
