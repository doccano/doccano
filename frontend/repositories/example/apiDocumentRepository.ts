import ApiService from '@/services/api.service'
import { ExampleRepository, SearchOption } from '~/domain/models/example/exampleRepository'
import { ExampleItem, ExampleItemList } from '~/domain/models/example/example'


export class APIExampleRepository implements ExampleRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async list(projectId: string, { limit = '10', offset = '0', q = '', isChecked = '', filterName = '' }: SearchOption): Promise<ExampleItemList> {
    const url = `/projects/${projectId}/docs?limit=${limit}&offset=${offset}&q=${q}&${filterName}=${isChecked}`
    const response = await this.request.get(url)
    return ExampleItemList.valueOf(response.data)
  }

  async create(projectId: string, item: ExampleItem): Promise<ExampleItem> {
    const url = `/projects/${projectId}/docs`
    const response = await this.request.post(url, item.toObject())
    return ExampleItem.valueOf(response.data)
  }

  async update(projectId: string, item: ExampleItem): Promise<ExampleItem> {
    const url = `/projects/${projectId}/docs/${item.id}`
    const response = await this.request.patch(url, item.toObject())
    return ExampleItem.valueOf(response.data)
  }

  async bulkDelete(projectId: string, ids: number[]): Promise<void> {
    const url = `/projects/${projectId}/docs`
    await this.request.delete(url, { ids })
  }

  async deleteAll(projectId: string): Promise<void> {
    const url = `/projects/${projectId}/docs`
    await this.request.delete(url)
  }

  async uploadFile(projectId: string, payload: FormData): Promise<void> {
    const url = `/projects/${projectId}/docs/upload`
    const config = {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }
    await this.request.post(url, payload, config)
  }

  async exportFile(projectId: string, format: string, onlyApproved: boolean): Promise<any> {
    const headers = { 'Content-Type': '', 'Accept': ''}
    if (format === 'csv') {
      headers.Accept = 'text/csv; charset=utf-8'
      headers['Content-Type'] = 'text/csv; charset=utf-8'
    } else if (format === 'txt') {
      headers.Accept = 'text/plain; charset=utf-8'
      headers['Content-Type'] = 'text/plain; charset=utf-8'
    } else {
      headers.Accept = 'application/json'
      headers['Content-Type'] = 'application/json'
    }
    const config = {
      responseType: 'blob',
      params: {
        q: format,
        onlyApproved
      },
      headers
    }
    const url = `/projects/${projectId}/docs/download`
    return await this.request.get(url, config)
  }

  async approve(projectId: string, docId: number, approved: boolean): Promise<void> {
    const url = `/projects/${projectId}/docs/${docId}/approve-labels`
    await this.request.post(url, { approved })
  }
}
