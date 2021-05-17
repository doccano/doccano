import ApiService from '@/services/api.service'
import { ExampleRepository, SearchOption } from '~/domain/models/example/exampleRepository'
import { ExampleItem, ExampleItemList } from '~/domain/models/example/example'


export class APIExampleRepository implements ExampleRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async list(projectId: string, { limit = '10', offset = '0', q = '', isChecked = '', filterName = '' }: SearchOption): Promise<ExampleItemList> {
    const url = `/projects/${projectId}/data?limit=${limit}&offset=${offset}&q=${q}&${filterName}=${isChecked}`
    const response = await this.request.get(url)
    return ExampleItemList.valueOf(response.data)
  }

  async create(projectId: string, item: ExampleItem): Promise<ExampleItem> {
    const url = `/projects/${projectId}/data`
    const response = await this.request.post(url, item.toObject())
    return ExampleItem.valueOf(response.data)
  }

  async update(projectId: string, item: ExampleItem): Promise<ExampleItem> {
    const url = `/projects/${projectId}/data/${item.id}`
    const response = await this.request.patch(url, item.toObject())
    return ExampleItem.valueOf(response.data)
  }

  async bulkDelete(projectId: string, ids: number[]): Promise<void> {
    const url = `/projects/${projectId}/data`
    await this.request.delete(url, { ids })
  }

  async deleteAll(projectId: string): Promise<void> {
    const url = `/projects/${projectId}/data`
    await this.request.delete(url)
  }

  async approve(projectId: string, docId: number, approved: boolean): Promise<void> {
    const url = `/projects/${projectId}/approval/${docId}`
    await this.request.post(url, { approved })
  }
}
